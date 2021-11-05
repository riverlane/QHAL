from typing import Dict, Tuple

import numpy as np

from . import command_unpacker, string_to_opcode
from ..quantum_simulators import IQuantumSimulator


class HALMetadata:
    """Class for storing HAL metadata items in pre-defined form.
    """
    def __init__(
        self,
        num_qubits: int = 0,
        max_depth: int = 0,
        native_gates: Dict[int, Tuple[int, np.array]] = {},
        connectivity: np.array = np.array([])
    ):

        def _error_raiser(metadata_item: str) -> None:
            raise ValueError(
                f"Metadata item {metadata_item} inconsistent with other items!"
            )

        self.num_qubits = num_qubits
        if max_depth > 0 and num_qubits == 0:
            _error_raiser("max_depth")
        else:
            self.max_depth = max_depth
        self.connectivity = connectivity if \
            connectivity.shape[0] == num_qubits \
            else _error_raiser("connectivity")
        self.native_gates = native_gates if \
            all([
                mat.shape[0] <= num_qubits for mat in
                [t[1] for t in native_gates.values()]
            ]) \
            else _error_raiser("native_gates")


class HardwareAbstractionLayer:
    """Encapsulates a process which receives HAL commands and uses them to
    perform operations on a quantum device.

    Parameters
    ----------
    quantum_simulator : IQuantumSimulator
        Object with the IQuantumSimulator interface that accepts commands
        and returns measurement results.
    hal_metadata : HALMetadata
        Object that holds a series of metadata items using a pre-defined
        structure.
    """

    def __init__(
        self,
        quantum_simulator: IQuantumSimulator,
        hal_metadata: HALMetadata
    ):
        self._quantum_simulator = quantum_simulator

        # set up some of the metadata in correct format
        self._hal_metadata = hal_metadata
        self._encoded_metadata = {}
        self._final_mask = (1 << 60)

        self._encoded_metadata["NUM_QUBITS"] = \
            (1 << 61) + self._hal_metadata.num_qubits
        self._encoded_metadata["MAX_DEPTH"] = \
            (2 << 61) + self._hal_metadata.max_depth

        native_gates = {}
        for i, (gate, gate_data) in enumerate(hal_metadata.native_gates.items()):
            native_gates[i] = []

            native_gates[i].append(
                (3 << 61) +
                (i << 57) +
                (string_to_opcode(gate).code << 45) +
                gate_data[0]
            )

        self._encoded_metadata["NATIVE_GATES"] = native_gates

        # useful state flags
        self._metadata_index = 0  # keep track of previously sent data chunk
        self._previous_metadata_request_index = 0  # previous metadata request index

    def accept_command(self, hal_command: np.uint64) -> np.uint64:
        """Interface for ``quantum_simulator.accept_command``.

        Parameters
        ----------
        command : uint64
            The HAL command to deconstruct and use to perform actions.

        Returns
        -------
        uint64
            Result of a measurement command or metadata request.
            NOTE: Metadata requests are designed to be streamed back as a
            series of 64-bit data chunks, while the caller waits for a flag
            that specifies the final chunk has been sent.
            Since this is a Python implementation we can't stream back
            multiple returns from a single function call, so the caller must
            simulate receiving the stream by sending multiple metadata request
            calls until the "final" flag is receieved.
        """

        # check if we've receieved a metadata request
        opcode, _, param, idx = command_unpacker(hal_command)
        if opcode == "REQUEST_METADATA":

            # reset the internal counter for streaming back data
            if param[0] != self._previous_metadata_request_index:
                self._metadata_index == 0

            if param[0] == 1:  # num_qubits request
                return self._encoded_metadata["NUM_QUBITS"] + self._final_mask

            elif param[0] == 2:  # max depth request
                return self._encoded_metadata["MAX_DEPTH"] + self._final_mask

            elif param[0] == 3:  # native gate request
                self._previous_metadata_request_index = param[0]

                if len(self._encoded_metadata["NATIVE_GATES"]) == 0:
                    return (3 << 61) + self._final_mask

                gate_list = [
                    i[0] for i in list(
                        self._encoded_metadata["NATIVE_GATES"].values()
                    )
                ]

                data = gate_list[self._metadata_index]
                self._metadata_index += 1
                if self._metadata_index == len(gate_list):
                    data = data + self._final_mask   # add final flag
                    self._metadata_index = 0
                return data

            elif param[0] == 4:  # connectivity matrix request

                def encode_connectivity_mat(upper_mat_array, row_index=None):

                    # get all non-zero off-diagonal indexes
                    row_col_indexes = np.transpose(np.nonzero(upper_mat_array))

                    encoded_metadata = []
                    encoded_indexes = 0
                    count = 2
                    for i, row_col in enumerate(row_col_indexes):

                        if len(row_col) > 1:
                            indexes = ((row_col[0] << 10) + row_col[1])
                        else:
                            indexes = ((row_index << 10) + row_col[0])

                        encoded_indexes += indexes << (count * 20)
                        count -= 1

                        if count == -1 or i == len(row_col_indexes) - 1:
                            encoded_metadata.append(
                                int(encoded_indexes) | (4 << 61)
                            )
                            encoded_indexes = 0
                            count = 2

                    return encoded_metadata

                if len(self._hal_metadata.connectivity) == 0:
                    return (4 << 61) + self._final_mask

                upper_mat_array = np.triu(self._hal_metadata.connectivity, 1)

                # are we requesting a single row?
                if param[1] >> 15:
                    row_index = idx[0] + idx[1]
                    upper_mat_array = upper_mat_array[row_index]
                    # build 64-bit encoded response
                    encoded_list = encode_connectivity_mat(
                        upper_mat_array, row_index
                    )

                else:  # request the whole matrix
                    # keep internal store so we dont construct every time
                    if "CONNECTIVITY" not in self._encoded_metadata:
                        # build 64-bit encoded response
                        self._encoded_metadata["CONNECTIVITY"] = \
                            encode_connectivity_mat(upper_mat_array)
                    encoded_list = self._encoded_metadata["CONNECTIVITY"]

                self._previous_metadata_request_index = param[0]

                data = encoded_list[self._metadata_index]
                self._metadata_index += 1
                if self._metadata_index == len(encoded_list):
                    data = data + self._final_mask  # add final flag
                    self._metadata_index = 0
                return int(data)

            elif param[0] == 5:  # error rate matrix request

                def encode_error_mat(error_rate_matrix):

                    # build up 64-bit encoded response
                    encoded_metadata = []
                    encoded_error_rates = 0
                    count = 3
                    for i, error_rate in enumerate(error_rate_matrix):

                        # encode the error rate (mantissa, exp)
                        exp = -1

                        while error_rate - int(error_rate) != 0:
                            if error_rate < 1:
                                exp += 1
                            error_rate = float(f'{error_rate:.3g}') * 10

                        encoded_error_rate = (int(error_rate) << 4) + exp

                        encoded_error_rates += \
                            int(encoded_error_rate) << (count * 14)
                        count -= 1

                        if count == -1 or i == len(error_rate_matrix) - 1:
                            encoded_metadata.append(
                                (5 << 61) | int(encoded_error_rates)
                            )
                            encoded_error_rates = 0
                            count = 3

                    return encoded_metadata

                if len(self._encoded_metadata["NATIVE_GATES"]) == 0:
                    return (5 << 61) + self._final_mask

                gate_index = param[1] >> 13
                diagonal = False

                error_rate_matrix = self._hal_metadata.native_gates[
                    list(self._hal_metadata.native_gates.keys())[gate_index]
                ][1]

                # are we requesting a single row?
                if (param[1] >> 12) & 1:

                    row_index = idx[0] + idx[1]

                    # set up data to be encoded
                    if len(error_rate_matrix.shape) > 1:  # 1- or 2-qubit gate?

                        mat_upper = np.triu(error_rate_matrix)
                        mat_lower = np.tril(error_rate_matrix)

                        new_mat = np.concatenate(
                            (
                                mat_upper[row_index],
                                np.transpose(mat_lower)[row_index]
                            )
                        )

                        c = np.nonzero(new_mat)
                        error_rate_matrix = new_mat[c]
                    else:
                        error_rate_matrix = [error_rate_matrix[row_index]]
                        diagonal = True

                    # build 64-bit encoded response
                    gate_data_list = encode_error_mat(error_rate_matrix)

                else:  # return thr whole matrix

                    gate_data_list = self._encoded_metadata["NATIVE_GATES"][
                        gate_index
                    ][1:]

                    # if there is no encoded data yet
                    # keep internal store so we dont construct every time
                    if len(gate_data_list) == 0:

                        # 1- or 2-qubit gate?
                        if len(error_rate_matrix.shape) > 1:

                            mat_upper = np.triu(error_rate_matrix)
                            mat_lower = np.tril(error_rate_matrix)

                            new_mat = np.concatenate(
                                (mat_upper, np.transpose(mat_lower)),
                                axis=1
                            )

                            r, c = np.nonzero(new_mat)
                            error_rate_matrix = new_mat[r, c]
                        else:
                            diagonal = True

                        # build 64-bit encoded response
                        gate_data_list.extend(
                            encode_error_mat(error_rate_matrix)
                        )

                self._previous_metadata_request_index = param[0]

                data = gate_data_list[self._metadata_index]
                data = data + (diagonal << 59)  # add diagonal flag
                data = data + (gate_index << 56)  # add gate index
                if self._metadata_index == len(gate_data_list) - 1:
                    data = data + self._final_mask  # add final flag
                    self._metadata_index = 0
                else:
                    self._metadata_index += 1
                return int(data)

        else:
            return self._quantum_simulator.accept_command(hal_command)
