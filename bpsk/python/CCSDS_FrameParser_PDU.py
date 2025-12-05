import pmt
from gnuradio import gr

class CCSDS_FrameParser_PDU(gr.basic_block):
    """
    Input PDU:  CCSDS packet (primary header + payload)
    Output PDU: CSP payload bytes (header stripped)
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="CCSDS_FrameParser_PDU",
            in_sig=None,
            out_sig=None)

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_pdu)
        self.message_port_register_out(pmt.intern('out'))

    def handle_pdu(self, pdu):
        meta = pmt.car(pdu)
        data = bytearray(pmt.u8vector_elements(pmt.cdr(pdu)))

        if len(data) < 6:
            # Not enough data, drop
            return

        # Parse length field
        pkt_len = (data[4] << 8) | data[5]
        expected_total = 6 + pkt_len + 1

        if len(data) < expected_total:
            # Incomplete / truncated packet, drop
            return

        payload = data[6:expected_total]

        out_vec = pmt.init_u8vector(len(payload), payload)
        out_pdu = pmt.cons(meta, out_vec)
        self.message_port_pub(pmt.intern('out'), out_pdu)
