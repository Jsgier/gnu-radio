import pmt
from gnuradio import gr

class CCSDS_FrameBuilder_PDU(gr.basic_block):
    """
    Input PDU:  CSP payload bytes (pmt.cons(meta, u8vector))
    Output PDU: CCSDS packet (primary header + payload)
    """
    def __init__(self, apid=0):
        gr.basic_block.__init__(self,
            name="CCSDS_FrameBuilder_PDU",
            in_sig=None,
            out_sig=None)

        self.apid = int(apid) & 0x7FF     # 11 bits
        self.seq_count = 0                # 14-bit counter

        # Register PDU ports
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_pdu)
        self.message_port_register_out(pmt.intern('out'))

    def handle_pdu(self, pdu):
        meta = pmt.car(pdu)
        data = bytearray(pmt.u8vector_elements(pmt.cdr(pdu)))

        # CCSDS primary header fields
        version = 0         # 3 bits
        pkt_type = 0        # 1 bit (0 = TM)
        sec_hdr_flag = 0    # 1 bit
        apid = self.apid    # 11 bits

        seq_flags = 3       # 2 bits (11 = standalone)
        seq_count = self.seq_count & 0x3FFF
        self.seq_count = (self.seq_count + 1) & 0x3FFF

        # packet length field: (total_packet_len - 1) - 6
        # total_packet_len = 6 (header) + len(data)
        pkt_len = len(data) - 1
        if pkt_len < 0:
            pkt_len = 0

        # Pack header (6 bytes)
        first_two = ((version & 0x7) << 13) | ((pkt_type & 0x1) << 12) | \
                    ((sec_hdr_flag & 0x1) << 11) | (apid & 0x7FF)
        second_two = ((seq_flags & 0x3) << 14) | (seq_count & 0x3FFF)

        header = bytearray(6)
        header[0] = (first_two >> 8) & 0xFF
        header[1] = first_two & 0xFF
        header[2] = (second_two >> 8) & 0xFF
        header[3] = second_two & 0xFF
        header[4] = (pkt_len >> 8) & 0xFF
        header[5] = pkt_len & 0xFF

        packet = header + data

        out_vec = pmt.init_u8vector(len(packet), packet)
        out_pdu = pmt.cons(meta, out_vec)
        self.message_port_pub(pmt.intern('out'), out_pdu)
