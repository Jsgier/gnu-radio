import pmt

class blk:
    """
    Prepend CCSDS ASM (0x1A CF FC 1D) to each PDU
    """

    def __init__(self):
        # Register message ports
        self.message_port_register_in(pmt.intern("in"))
        self.message_port_register_out(pmt.intern("out"))

        # Assign handler
        self.set_msg_handler(pmt.intern("in"), self.handle_msg)

    def handle_msg(self, msg):
        """
        msg is a PDU: (metadata, u8vector)
        We prepend the 4-byte CCSDS ASM and emit a new PDU.
        """
        meta = pmt.car(msg)
        vec = pmt.cdr(msg)

        # Convert the PMT vector to Python bytes
        payload = bytes(pmt.u8vector_elements(vec))

        # CCSDS Attached Sync Marker (ASM)
        asm = bytes([0x1A, 0xCF, 0xFC, 0x1D])

        # Create new payload
        out_bytes = asm + payload

        # Convert back to PMT
        out_vec = pmt.init_u8vector(len(out_bytes), out_bytes)
        out_pdu = pmt.cons(meta, out_vec)

        # Publish
        self.message_port_pub(pmt.intern("out"), out_pdu)
