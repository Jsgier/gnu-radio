import pmt
from gnuradio import gr

# You need `pip install reedsolo` in your GNU Radio Python environment
import reedsolo

class RS223_255_Interleaver_Enc_PDU(gr.basic_block):
    """
    Input PDU:  CCSDS frame bytes (arbitrary length)
    Output PDU: interleaved RS(223,255) codewords in bytes

    - Breaks input into 223-byte blocks (pads last if needed)
    - Encodes each with RS(223,255)
    - Interleaves codewords with given depth
    """
    def __init__(self, depth=5):
        gr.basic_block.__init__(self,
            name="RS223_255_Interleaver_Enc_PDU",
            in_sig=None,
            out_sig=None)

        self.depth = int(depth)
        self.rs = reedsolo.RSCodec(32)  # 255 - 223 = 32 parity bytes

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_pdu)
        self.message_port_register_out(pmt.intern('out'))

    def _encode_blocks(self, data):
        blocks = []
        for i in range(0, len(data), 223):
            block = bytearray(data[i:i+223])
            if len(block) < 223:
                # pad with zeros at the end
                block.extend([0] * (223 - len(block)))
            enc = self.rs.encode(bytes(block))  # 255 bytes
            blocks.append(bytearray(enc))
        return blocks

    def _interleave(self, codewords):
        """
        Simple block interleaver: take groups of `depth` codewords,
        write them row-wise into matrix, read out column-wise.
        """
        if self.depth <= 1:
            # no interleaving
            out = bytearray()
            for cw in codewords:
                out.extend(cw)
            return out

        out = bytearray()
        n = len(codewords)
        cw_len = len(codewords[0])

        for start in range(0, n, self.depth):
            group = codewords[start:start + self.depth]
            # pad group if incomplete
            if len(group) < self.depth:
                pad_cw = bytearray([0]*cw_len)
                while len(group) < self.depth:
                    group.append(pad_cw)

            # interleave: columns first
            for col in range(cw_len):
                for row in range(self.depth):
                    out.append(group[row][col])

        return out

    def handle_pdu(self, pdu):
        meta = pmt.car(pdu)
        data = bytearray(pmt.u8vector_elements(pmt.cdr(pdu)))

        codewords = self._encode_blocks(data)
        interleaved = self._interleave(codewords)

        out_vec = pmt.init_u8vector(len(interleaved), interleaved)
        out_pdu = pmt.cons(meta, out_vec)
        self.message_port_pub(pmt.intern('out'), out_pdu)
