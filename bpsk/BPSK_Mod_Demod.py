#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: BPSK Modulator / Demodulator
# Author: J. Gier
# GNU Radio version: 3.10.12.0

from gnuradio import blocks
from gnuradio import blocks, gr
from gnuradio import digital
from gnuradio import fec
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from gnuradio import zeromq
import BPSK_Mod_Demod_epy_block_0 as epy_block_0  # embedded python block
import BPSK_Mod_Demod_epy_block_1 as epy_block_1  # embedded python block
import BPSK_Mod_Demod_epy_block_2 as epy_block_2  # embedded python block
import BPSK_Mod_Demod_epy_block_3 as epy_block_3  # embedded python block
import satellites
import threading




class BPSK_Mod_Demod(gr.top_block):

    def __init__(self, frame_size=100, puncpat='11'):
        gr.top_block.__init__(self, "BPSK Modulator / Demodulator", catch_exceptions=True)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Parameters
        ##################################################
        self.frame_size = frame_size
        self.puncpat = puncpat

        ##################################################
        # Variables
        ##################################################
        self.payload_len_int = payload_len_int = 223
        self.payload_coded_len = payload_coded_len = payload_len_int + 32
        self.depth = depth = 1
        self.frame_bytes = frame_bytes = payload_coded_len* depth
        self.sps = sps = 4
        self.samp_rate = samp_rate = 20E6
        self.nfilts = nfilts = 32
        self.frame_bits = frame_bits = frame_bytes*8
        self.excess_bw = excess_bw = 0.250
        self.symbol_rate = symbol_rate = samp_rate/sps
        self.source_address = source_address = "tcp://127.0.0.1:5555"
        self.sink_address = sink_address = "tcp://127.0.0.1:5556"
        self.rs_generator = rs_generator = 291
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), excess_bw, nfilts*11*sps)
        self.prim_element = prim_element = 2
        self.phase_bw = phase_bw = 2*3.14/100
        self.nroots = nroots = 32
        self.len_tag_key_bits = len_tag_key_bits = "frame_len_bits"
        self.len_tag_key = len_tag_key = "frame_len"
        self.gen_poly = gen_poly = 285
        self.frame_len = frame_len = 2072
        self.format_key = format_key = "protocol_packet"
        self.first_root = first_root = 112
        self.delay_constellation = delay_constellation = 32
        self.delay_byte = delay_byte = 33
        self.delay_bit = delay_bit = 24
        self.decode_bits = decode_bits = int(frame_bits/8)
        self.cc_enc_def = cc_enc_def = fec.cc_encoder_make((frame_size * 8 ),7, 2, [-109,79], 0, fec.CC_STREAMING, False)
        self.cc_dec_def = cc_dec_def = fec.cc_decoder.make((frame_size  * 8 ),7, 2, [-109,79], 0, (-1), fec.CC_STREAMING, False)
        self.bpsk = bpsk = digital.constellation_bpsk().base()
        self.bpsk.set_npwr(1.0)
        self.access_code = access_code = 0o00011010110011111111110000011101

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_push_msg_sink_1 = zeromq.push_msg_sink(sink_address, 100, True)
        self.zeromq_pull_msg_source_1 = zeromq.pull_msg_source(source_address, 100, True)
        self.satellites_encode_rs_ccsds_0 = satellites.encode_rs(False, 1)
        self.satellites_decode_rs_ccsds_0 = satellites.decode_rs(False, 1)
        self.pdu_tagged_stream_to_pdu_0_0_0_0 = pdu.tagged_stream_to_pdu(gr.types.byte_t, "frame_len")
        self.pdu_pdu_to_tagged_stream_0_0_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, "stream_tag")
        self.fec_extended_encoder_1_0_0 = fec.extended_encoder(encoder_obj_list=cc_enc_def, threading='capillary', puncpat=puncpat)
        self.fec_extended_decoder_0_1_0 = fec.extended_decoder(decoder_obj_list=cc_dec_def, threading='capillary', ann=None, puncpat=puncpat, integration_period=10000)
        self.epy_block_3 = epy_block_3.blk(verbose=True)
        self.epy_block_2 = epy_block_2.blk(verbose=True)
        self.epy_block_1 = epy_block_1.blk(frame_len=frame_len, verbose=True)
        self.epy_block_0 = epy_block_0.blk()
        self.digital_scrambler_bb_0 = digital.scrambler_bb(0x9A, 0xFF, 7)
        self.digital_pfb_clock_sync_xxx_0_0 = digital.pfb_clock_sync_ccf(sps, excess_bw, rrc_taps, nfilts, 0, 1.5, 1)
        self.digital_map_bb_0_0_0_0 = digital.map_bb([-1,1])
        self.digital_descrambler_bb_0 = digital.descrambler_bb(0x9A, 0xFF, 7)
        self.digital_costas_loop_cc_0_0 = digital.costas_loop_cc(0.2, 4, True)
        self.digital_correlate_access_code_tag_xx_0 = digital.correlate_access_code_tag_bb('0o00011010110011111111110000011101', 2, 'CCSDS_frame')
        self.digital_constellation_modulator_0_0 = digital.generic_mod(
            constellation=bpsk,
            differential=False,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=excess_bw,
            verbose=False,
            log=False,
            truncate=False)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(bpsk)
        self.blocks_unpack_k_bits_bb_2_1 = blocks.unpack_k_bits_bb(8)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_tagged_stream_align_1 = blocks.tagged_stream_align(gr.sizeof_char*1, "frame_len")
        self.blocks_pack_k_bits_bb_1_0 = blocks.pack_k_bits_bb(8)
        self.blocks_message_debug_0_1_0_0_0 = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_message_debug_0_1_0_0_0.set_block_alias("Input")
        self.blocks_delay_3 = blocks.delay(gr.sizeof_gr_complex*1, 3)
        self.blocks_char_to_float_0_2_0 = blocks.char_to_float(1, 1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0, 'out'), (self.pdu_pdu_to_tagged_stream_0_0_0, 'pdus'))
        self.msg_connect((self.epy_block_2, 'out'), (self.satellites_decode_rs_ccsds_0, 'in'))
        self.msg_connect((self.epy_block_3, 'out'), (self.epy_block_2, 'in'))
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0_0_0_0, 'pdus'), (self.epy_block_3, 'in'))
        self.msg_connect((self.satellites_decode_rs_ccsds_0, 'out'), (self.blocks_message_debug_0_1_0_0_0, 'print'))
        self.msg_connect((self.satellites_decode_rs_ccsds_0, 'out'), (self.zeromq_push_msg_sink_1, 'in'))
        self.msg_connect((self.satellites_encode_rs_ccsds_0, 'out'), (self.epy_block_0, 'in'))
        self.msg_connect((self.zeromq_pull_msg_source_1, 'out'), (self.satellites_encode_rs_ccsds_0, 'in'))
        self.connect((self.blocks_char_to_float_0_2_0, 0), (self.fec_extended_decoder_0_1_0, 0))
        self.connect((self.blocks_delay_3, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_1_0, 0), (self.digital_constellation_modulator_0_0, 0))
        self.connect((self.blocks_tagged_stream_align_1, 0), (self.pdu_tagged_stream_to_pdu_0_0_0_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.digital_pfb_clock_sync_xxx_0_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_2_1, 0), (self.digital_scrambler_bb_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_map_bb_0_0_0_0, 0))
        self.connect((self.digital_constellation_modulator_0_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.digital_correlate_access_code_tag_xx_0, 0), (self.epy_block_1, 0))
        self.connect((self.digital_costas_loop_cc_0_0, 0), (self.blocks_delay_3, 0))
        self.connect((self.digital_descrambler_bb_0, 0), (self.digital_correlate_access_code_tag_xx_0, 0))
        self.connect((self.digital_map_bb_0_0_0_0, 0), (self.blocks_char_to_float_0_2_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0_0, 0), (self.digital_costas_loop_cc_0_0, 0))
        self.connect((self.digital_scrambler_bb_0, 0), (self.fec_extended_encoder_1_0_0, 0))
        self.connect((self.epy_block_1, 0), (self.blocks_tagged_stream_align_1, 0))
        self.connect((self.fec_extended_decoder_0_1_0, 0), (self.digital_descrambler_bb_0, 0))
        self.connect((self.fec_extended_encoder_1_0_0, 0), (self.blocks_pack_k_bits_bb_1_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0_0_0, 0), (self.blocks_unpack_k_bits_bb_2_1, 0))


    def get_frame_size(self):
        return self.frame_size

    def set_frame_size(self, frame_size):
        self.frame_size = frame_size

    def get_puncpat(self):
        return self.puncpat

    def set_puncpat(self, puncpat):
        self.puncpat = puncpat

    def get_payload_len_int(self):
        return self.payload_len_int

    def set_payload_len_int(self, payload_len_int):
        self.payload_len_int = payload_len_int
        self.set_payload_coded_len(self.payload_len_int + 32)

    def get_payload_coded_len(self):
        return self.payload_coded_len

    def set_payload_coded_len(self, payload_coded_len):
        self.payload_coded_len = payload_coded_len
        self.set_frame_bytes(self.payload_coded_len* self.depth)

    def get_depth(self):
        return self.depth

    def set_depth(self, depth):
        self.depth = depth
        self.set_frame_bytes(self.payload_coded_len* self.depth)

    def get_frame_bytes(self):
        return self.frame_bytes

    def set_frame_bytes(self, frame_bytes):
        self.frame_bytes = frame_bytes
        self.set_frame_bits(self.frame_bytes*8)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.excess_bw, self.nfilts*11*self.sps))
        self.set_symbol_rate(self.samp_rate/self.sps)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_symbol_rate(self.samp_rate/self.sps)
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.excess_bw, self.nfilts*11*self.sps))

    def get_frame_bits(self):
        return self.frame_bits

    def set_frame_bits(self, frame_bits):
        self.frame_bits = frame_bits
        self.set_decode_bits(int(self.frame_bits/8))

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.excess_bw, self.nfilts*11*self.sps))
        self.digital_pfb_clock_sync_xxx_0_0.set_loop_bandwidth(self.excess_bw)

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate

    def get_source_address(self):
        return self.source_address

    def set_source_address(self, source_address):
        self.source_address = source_address

    def get_sink_address(self):
        return self.sink_address

    def set_sink_address(self, sink_address):
        self.sink_address = sink_address

    def get_rs_generator(self):
        return self.rs_generator

    def set_rs_generator(self, rs_generator):
        self.rs_generator = rs_generator

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_0_0.update_taps(self.rrc_taps)

    def get_prim_element(self):
        return self.prim_element

    def set_prim_element(self, prim_element):
        self.prim_element = prim_element

    def get_phase_bw(self):
        return self.phase_bw

    def set_phase_bw(self, phase_bw):
        self.phase_bw = phase_bw

    def get_nroots(self):
        return self.nroots

    def set_nroots(self, nroots):
        self.nroots = nroots

    def get_len_tag_key_bits(self):
        return self.len_tag_key_bits

    def set_len_tag_key_bits(self, len_tag_key_bits):
        self.len_tag_key_bits = len_tag_key_bits

    def get_len_tag_key(self):
        return self.len_tag_key

    def set_len_tag_key(self, len_tag_key):
        self.len_tag_key = len_tag_key

    def get_gen_poly(self):
        return self.gen_poly

    def set_gen_poly(self, gen_poly):
        self.gen_poly = gen_poly

    def get_frame_len(self):
        return self.frame_len

    def set_frame_len(self, frame_len):
        self.frame_len = frame_len
        self.epy_block_1.frame_len = self.frame_len

    def get_format_key(self):
        return self.format_key

    def set_format_key(self, format_key):
        self.format_key = format_key

    def get_first_root(self):
        return self.first_root

    def set_first_root(self, first_root):
        self.first_root = first_root

    def get_delay_constellation(self):
        return self.delay_constellation

    def set_delay_constellation(self, delay_constellation):
        self.delay_constellation = delay_constellation

    def get_delay_byte(self):
        return self.delay_byte

    def set_delay_byte(self, delay_byte):
        self.delay_byte = delay_byte

    def get_delay_bit(self):
        return self.delay_bit

    def set_delay_bit(self, delay_bit):
        self.delay_bit = delay_bit

    def get_decode_bits(self):
        return self.decode_bits

    def set_decode_bits(self, decode_bits):
        self.decode_bits = decode_bits

    def get_cc_enc_def(self):
        return self.cc_enc_def

    def set_cc_enc_def(self, cc_enc_def):
        self.cc_enc_def = cc_enc_def

    def get_cc_dec_def(self):
        return self.cc_dec_def

    def set_cc_dec_def(self, cc_dec_def):
        self.cc_dec_def = cc_dec_def

    def get_bpsk(self):
        return self.bpsk

    def set_bpsk(self, bpsk):
        self.bpsk = bpsk
        self.digital_constellation_decoder_cb_0.set_constellation(self.bpsk)

    def get_access_code(self):
        return self.access_code

    def set_access_code(self, access_code):
        self.access_code = access_code



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--frame-size", dest="frame_size", type=intx, default=100,
        help="Set Frame Size [default=%(default)r]")
    return parser


def main(top_block_cls=BPSK_Mod_Demod, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(frame_size=options.frame_size)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    tb.flowgraph_started.set()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
