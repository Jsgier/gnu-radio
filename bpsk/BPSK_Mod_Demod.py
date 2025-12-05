#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: BPSK Modulator / Demodulator
# Author: J. Gier
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
from gnuradio import blocks, gr
from gnuradio import digital
from gnuradio import fec
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
import BPSK_Mod_Demod_epy_block_0_0 as epy_block_0_0  # embedded python block
import satellites
import threading



class BPSK_Mod_Demod(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "BPSK Modulator / Demodulator", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("BPSK Modulator / Demodulator")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "BPSK_Mod_Demod")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.payload_len_int = payload_len_int = 200
        self.payload_coded_len = payload_coded_len = payload_len_int + 32
        self.depth = depth = 2
        self.frame_bytes = frame_bytes = payload_coded_len* depth
        self.sps = sps = 4
        self.nfilts = nfilts = 16
        self.frame_bits = frame_bits = frame_bytes*8
        self.excess_bw = excess_bw = 0.220
        self.samp_rate = samp_rate = 10000000
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), excess_bw, 11*sps*nfilts)
        self.prim_element = prim_element = 2
        self.phase_bw = phase_bw = 62.8e-3
        self.packet_len_key = packet_len_key = "packet_len"
        self.nroots = nroots = 32
        self.len_tag_key = len_tag_key = "payload_coded_len"
        self.gen_poly = gen_poly = 285
        self.first_root = first_root = 1
        self.delay = delay = int((1.875*sps+7)*2)
        self.decode_bits = decode_bits = int(frame_bits/8)
        self.cc_enc_def = cc_enc_def = fec.cc_encoder_make(frame_bits,7, 2, [121,91], 0, fec.CC_STREAMING, True)
        self.cc_dec_def = cc_dec_def = fec.cc_decoder.make(frame_bits,7, 2, [121,91], 0, 0, fec.CC_STREAMING, True)
        self.bpsk = bpsk = digital.constellation_bpsk().base()
        self.bpsk.set_npwr(1.0)

        ##################################################
        # Blocks
        ##################################################

        self.satellites_encode_rs_0 = satellites.encode_rs(8, gen_poly, first_root, prim_element, nroots, 1)
        self.satellites_decode_rs_0 = satellites.decode_rs(8, gen_poly, first_root, prim_element, nroots, 1)
        self.pdu_tagged_stream_to_pdu_0_0_0 = pdu.tagged_stream_to_pdu(gr.types.byte_t, "frame_len")
        self.pdu_pdu_to_tagged_stream_0_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, "frame_len")
        self.fec_extended_encoder_0 = fec.extended_encoder(encoder_obj_list=cc_enc_def, threading='capillary', puncpat='11')
        self.fec_extended_decoder_0 = fec.extended_decoder(decoder_obj_list=cc_dec_def, threading='capillary', ann=None, puncpat='11', integration_period=10000)
        self.epy_block_0_0 = epy_block_0_0.TestPatternSource_PDU(payload_len=payload_len_int, interval_ms=100)
        self.digital_map_bb_0 = digital.map_bb([-1,1])
        self.blocks_throttle2_0_0 = blocks.throttle( gr.sizeof_char*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_repack_bits_bb_1_0 = blocks.repack_bits_bb(1, 8, "frame_len", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_0 = blocks.repack_bits_bb(8, 1, "frame_len", False, gr.GR_MSB_FIRST)
        self.blocks_message_debug_0_1 = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0_0, 'out'), (self.satellites_encode_rs_0, 'in'))
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0_0_0, 'pdus'), (self.satellites_decode_rs_0, 'in'))
        self.msg_connect((self.satellites_decode_rs_0, 'out'), (self.blocks_message_debug_0_1, 'print'))
        self.msg_connect((self.satellites_encode_rs_0, 'out'), (self.pdu_pdu_to_tagged_stream_0_0, 'pdus'))
        self.connect((self.blocks_char_to_float_0, 0), (self.fec_extended_decoder_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0, 0), (self.fec_extended_encoder_0, 0))
        self.connect((self.blocks_repack_bits_bb_1_0, 0), (self.pdu_tagged_stream_to_pdu_0_0_0, 0))
        self.connect((self.blocks_throttle2_0_0, 0), (self.digital_map_bb_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.fec_extended_decoder_0, 0), (self.blocks_repack_bits_bb_1_0, 0))
        self.connect((self.fec_extended_encoder_0, 0), (self.blocks_throttle2_0_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0_0, 0), (self.blocks_repack_bits_bb_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "BPSK_Mod_Demod")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_payload_len_int(self):
        return self.payload_len_int

    def set_payload_len_int(self, payload_len_int):
        self.payload_len_int = payload_len_int
        self.set_payload_coded_len(self.payload_len_int + 32)
        self.epy_block_0_0.payload_len = self.payload_len_int

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
        self.set_delay(int((1.875*self.sps+7)*2))
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.excess_bw, 11*self.sps*self.nfilts))

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.excess_bw, 11*self.sps*self.nfilts))

    def get_frame_bits(self):
        return self.frame_bits

    def set_frame_bits(self, frame_bits):
        self.frame_bits = frame_bits
        self.set_decode_bits(int(self.frame_bits/8))

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.excess_bw, 11*self.sps*self.nfilts))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0_0.set_sample_rate(self.samp_rate)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps

    def get_prim_element(self):
        return self.prim_element

    def set_prim_element(self, prim_element):
        self.prim_element = prim_element

    def get_phase_bw(self):
        return self.phase_bw

    def set_phase_bw(self, phase_bw):
        self.phase_bw = phase_bw

    def get_packet_len_key(self):
        return self.packet_len_key

    def set_packet_len_key(self, packet_len_key):
        self.packet_len_key = packet_len_key

    def get_nroots(self):
        return self.nroots

    def set_nroots(self, nroots):
        self.nroots = nroots

    def get_len_tag_key(self):
        return self.len_tag_key

    def set_len_tag_key(self, len_tag_key):
        self.len_tag_key = len_tag_key

    def get_gen_poly(self):
        return self.gen_poly

    def set_gen_poly(self, gen_poly):
        self.gen_poly = gen_poly

    def get_first_root(self):
        return self.first_root

    def set_first_root(self, first_root):
        self.first_root = first_root

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay

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




def main(top_block_cls=BPSK_Mod_Demod, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
