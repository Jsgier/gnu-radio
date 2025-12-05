import pmt
from gnuradio import gr
import reedsolo

class RS223_255_Deinterleave_Dec_PDU(gr.basic_block):
    """
    Input PDU: interleaved RS(223,255) codewords (bytes)
    Output PDU: deinterleaved & RS-decoded bytes (original before RS+interleave)

    Assumes same interleaver depth as encoder.
    """
    def __init__(self, depth=5):
        gr.basic_block.__init__(self,
            name="RS223_255_Deinterleave_Dec_PDU",
            in_sig=None,
            out_sig=None)

        self.depth = int(depth)
        self.rs = reedsolo.RSCodec(32)

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_pdu)
        self.message_port_register_out(pmt.intern('out'))

    def _deinterleave(self, data):
        """
        Inverse of encoder's _interleave.
        Returns a list of 255-byte codewords.
        """
        if self.depth <= 1:
            # no interleaving
            if len(data) % 255 != 0:
                # truncate partial
                data = data[:len(data) - (len(data) % 255)]
            codewords = []
            for i in range(0, len(data), 255):
                codewords.append(bytearray(data[i:i+255]))
            return codewords

        cw_len = 255
        group_size = self.depth * cw_len
        codewords = []

        idx = 0
        while idx + group_size <= len(data):
            group_bytes = data[idx:idx + group_size]
            idx += group_size

            # reconstruct matrix: columns x rows
            # we read out in columns: for each col, depth rows
            # So we fill matrix[col][row]
            matrix = [[0 for _ in range(self.depth)] for _ in range(cw_len)]
            p = 0
            for col in range(cw_len):
                for row in range(self.depth):
                    matrix[col][row] = group_bytes[p]
                    p += 1

            # Now read out row-wise to get codewords
            for row in range(self.depth):
                cw = bytearray(cw_len)
                for col in range(cw_len):
                    cw[col] = matrix[col][row]
                codewords.append(cw)

        return codewords

    def _decode_blocks(self, codewords):
        out = bytearray()
        for cw in codewords:
            try:
                dec = self.rs.decode(bytes(cw))  # returns original 223 bytes
                out.extend(dec)
            except reedsolo.ReedSolomonError:
                # drop or append zeros on failure; here we drop
                pass
        return out

    def handle_pdu(self, pdu):
        meta = pmt.car(pdu)
        data = bytearray(pmt.u8vector_elements(pmt.cdr(pdu)))

        codewords = self._deinterleave(data)
        decoded = self._decode_blocks(codewords)

        out_vec = pmt.init_u8vector(len(decoded), decoded)
        out_pdu = pmt.cons(meta, out_vec)
        self.message_port_pub(pmt.intern('out'), out_pdu)
