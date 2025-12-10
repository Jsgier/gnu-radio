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
from PyQt5 import QtCore
from gnuradio import blocks
from gnuradio import blocks, gr
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import digital
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
import BPSK_Mod_Demod_epy_block_0 as epy_block_0  # embedded python block
import BPSK_Mod_Demod_epy_block_0_0_0 as epy_block_0_0_0  # embedded python block
import BPSK_Mod_Demod_epy_block_1 as epy_block_1  # embedded python block
import BPSK_Mod_Demod_epy_block_3 as epy_block_3  # embedded python block
import sip
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
        self.payload_len_int = payload_len_int = 223
        self.payload_coded_len = payload_coded_len = payload_len_int + 32
        self.depth = depth = 1
        self.frame_bytes = frame_bytes = payload_coded_len* depth
        self.sps = sps = 4
        self.samp_rate = samp_rate = 1000000
        self.nfilts = nfilts = 16
        self.frame_bits = frame_bits = frame_bytes*8
        self.excess_bw = excess_bw = 0.250
        self.time_offset = time_offset = 1
        self.symbol_rate = symbol_rate = samp_rate/sps
        self.rs_generator = rs_generator = 291
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), excess_bw, 11*sps*nfilts)
        self.prim_element = prim_element = 2
        self.phase_bw = phase_bw = 2*3.14/100
        self.nroots = nroots = 32
        self.noise_volt = noise_volt = 10E-3
        self.len_tag_key_bits = len_tag_key_bits = "frame_len_bits"
        self.len_tag_key = len_tag_key = "frame_len"
        self.gen_poly = gen_poly = 285
        self.freq_offset = freq_offset = 0
        self.format_key = format_key = "protocol_packet"
        self.first_root = first_root = 112
        self.delay = delay = 30
        self.decode_bits = decode_bits = int(frame_bits/8)
        self.bpsk = bpsk = digital.constellation_bpsk().base()
        self.bpsk.set_npwr(1.0)
        self.access_code = access_code = 0o00011010110011111111110000011101

        ##################################################
        # Blocks
        ##################################################

        self._time_offset_range = qtgui.Range(0.999, 1.001, 100e-6, 1, 200)
        self._time_offset_win = qtgui.RangeWidget(self._time_offset_range, self.set_time_offset, "Channel: time offset", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._time_offset_win)
        self._noise_volt_range = qtgui.Range(0, 500e-3, 100e-3, 10E-3, 200)
        self._noise_volt_win = qtgui.RangeWidget(self._noise_volt_range, self.set_noise_volt, "Channel: Noise Voltage", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._noise_volt_win)
        self._freq_offset_range = qtgui.Range(-100e-2 * (1/samp_rate), 100e-2 * (1/samp_rate), 10e-2 * (1/samp_rate), 0, 200)
        self._freq_offset_win = qtgui.RangeWidget(self._freq_offset_range, self.set_freq_offset, "Channel: Freq Offset", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._freq_offset_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 2)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(0.05)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 1, 0, 1, 4)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0_0_0_0 = qtgui.const_sink_c(
            2056, #size
            'bpsk_mod', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_0_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0_0_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0_0_0_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0_0_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0_0_0.enable_grid(False)
        self.qtgui_const_sink_x_0_0_0_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_0_0_0_win)
        self.qtgui_const_sink_x_0_0_0 = qtgui.const_sink_c(
            2056, #size
            'post_clock_sync', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0_0_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0_0.enable_grid(False)
        self.qtgui_const_sink_x_0_0_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_0_0_win)
        self.pdu_tagged_stream_to_pdu_0_0_0_0 = pdu.tagged_stream_to_pdu(gr.types.byte_t, "frame_len")
        self.pdu_pdu_to_tagged_stream_0_0_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, "stream_tag")
        self.epy_block_3 = epy_block_3.blk(verbose=True)
        self.epy_block_1 = epy_block_1.blk(frame_len=1816, verbose=True)
        self.epy_block_0_0_0 = epy_block_0_0_0.TestPatternSource_PDU(payload_len=payload_len_int, interval_ms=100)
        self.epy_block_0 = epy_block_0.blk()
        self.digital_pfb_clock_sync_xxx_0_0 = digital.pfb_clock_sync_ccf(sps, excess_bw, rrc_taps, 16, 8, 1.5, 1)
        self.digital_costas_loop_cc_0_0 = digital.costas_loop_cc(phase_bw, 4, True)
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
        self.digital_constellation_decoder_cb_0_0 = digital.constellation_decoder_cb(bpsk)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=noise_volt,
            frequency_offset=freq_offset,
            epsilon=time_offset,
            taps=[1.0],
            noise_seed=0,
            block_tags=False)
        self.blocks_xor_xx_0 = blocks.xor_bb()
        self.blocks_unpack_k_bits_bb_1_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_throttle2_0_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_tagged_stream_align_1 = blocks.tagged_stream_align(gr.sizeof_char*1, "frame_len")
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(0.010)
        self.blocks_message_debug_0_1_0_0 = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_message_debug_0_1_0_0.set_block_alias("Output")
        self.blocks_integrate_xx_0 = blocks.integrate_ff(100, 1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_char*1, delay)
        self.blocks_char_to_float_0_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.BER = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1,
            None # parent
        )
        self.BER.set_update_time(0.10)
        self.BER.set_title('BER')

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.BER.set_min(i, -1)
            self.BER.set_max(i, 1)
            self.BER.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.BER.set_label(i, "Data {0}".format(i))
            else:
                self.BER.set_label(i, labels[i])
            self.BER.set_unit(i, units[i])
            self.BER.set_factor(i, factor[i])

        self.BER.enable_autoscale(True)
        self._BER_win = sip.wrapinstance(self.BER.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._BER_win)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0, 'out'), (self.pdu_pdu_to_tagged_stream_0_0_0, 'pdus'))
        self.msg_connect((self.epy_block_0_0_0, 'out'), (self.epy_block_0, 'in'))
        self.msg_connect((self.epy_block_3, 'out'), (self.blocks_message_debug_0_1_0_0, 'print'))
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0_0_0_0, 'pdus'), (self.epy_block_3, 'in'))
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_char_to_float_0_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_char_to_float_0_0_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_char_to_float_0_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_xor_xx_0, 1))
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.BER, 0))
        self.connect((self.blocks_tagged_stream_align_1, 0), (self.pdu_tagged_stream_to_pdu_0_0_0_0, 0))
        self.connect((self.blocks_throttle2_0_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_1_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_xor_xx_0, 0), (self.blocks_char_to_float_0_0_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.digital_pfb_clock_sync_xxx_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0, 0), (self.blocks_xor_xx_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0, 0), (self.digital_correlate_access_code_tag_xx_0, 0))
        self.connect((self.digital_constellation_modulator_0_0, 0), (self.blocks_throttle2_0_0, 0))
        self.connect((self.digital_constellation_modulator_0_0, 0), (self.qtgui_const_sink_x_0_0_0_0, 0))
        self.connect((self.digital_constellation_modulator_0_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.digital_correlate_access_code_tag_xx_0, 0), (self.epy_block_1, 0))
        self.connect((self.digital_costas_loop_cc_0_0, 0), (self.digital_constellation_decoder_cb_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0, 0), (self.qtgui_const_sink_x_0_0_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0_0, 0), (self.digital_costas_loop_cc_0_0, 0))
        self.connect((self.epy_block_1, 0), (self.blocks_tagged_stream_align_1, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0_0_0, 0), (self.blocks_unpack_k_bits_bb_1_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0_0_0, 0), (self.digital_constellation_modulator_0_0, 0))


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
        self.epy_block_0_0_0.payload_len = self.payload_len_int

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
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.excess_bw, 11*self.sps*self.nfilts))
        self.set_symbol_rate(self.samp_rate/self.sps)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_symbol_rate(self.samp_rate/self.sps)
        self.blocks_throttle2_0_0.set_sample_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

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
        self.digital_pfb_clock_sync_xxx_0_0.set_loop_bandwidth(self.excess_bw)

    def get_time_offset(self):
        return self.time_offset

    def set_time_offset(self, time_offset):
        self.time_offset = time_offset
        self.channels_channel_model_0.set_timing_offset(self.time_offset)

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate

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
        self.digital_costas_loop_cc_0_0.set_loop_bandwidth(self.phase_bw)

    def get_nroots(self):
        return self.nroots

    def set_nroots(self, nroots):
        self.nroots = nroots

    def get_noise_volt(self):
        return self.noise_volt

    def set_noise_volt(self, noise_volt):
        self.noise_volt = noise_volt
        self.channels_channel_model_0.set_noise_voltage(self.noise_volt)

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

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.channels_channel_model_0.set_frequency_offset(self.freq_offset)

    def get_format_key(self):
        return self.format_key

    def set_format_key(self, format_key):
        self.format_key = format_key

    def get_first_root(self):
        return self.first_root

    def set_first_root(self, first_root):
        self.first_root = first_root

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay
        self.blocks_delay_0.set_dly(int(self.delay))

    def get_decode_bits(self):
        return self.decode_bits

    def set_decode_bits(self, decode_bits):
        self.decode_bits = decode_bits

    def get_bpsk(self):
        return self.bpsk

    def set_bpsk(self, bpsk):
        self.bpsk = bpsk
        self.digital_constellation_decoder_cb_0_0.set_constellation(self.bpsk)

    def get_access_code(self):
        return self.access_code

    def set_access_code(self, access_code):
        self.access_code = access_code




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
