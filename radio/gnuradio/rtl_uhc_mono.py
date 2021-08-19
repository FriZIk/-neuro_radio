#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: bpqvg
# GNU Radio version: 3.8.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import osmosdr
import time

from gnuradio import qtgui

class rtl_uhc_mono(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
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

        self.settings = Qt.QSettings("GNU Radio", "rtl_uhc_mono")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.volume = volume = 1
        self.transition = transition = 1000000
        self.samp_rate = samp_rate = 2048000
        self.quadrature = quadrature = 500000
        self.freq = freq = 101.9e6
        self.cutoff = cutoff = 100000
        self.audio_dec = audio_dec = 10

        ##################################################
        # Blocks
        ##################################################
        self._samp_rate_range = Range(24000, 4096000, 1000, 2048000, 200)
        self._samp_rate_win = RangeWidget(self._samp_rate_range, self.set_samp_rate, 'samp_rate', "counter_slider", float)
        self.top_grid_layout.addWidget(self._samp_rate_win)
        # Create the options list
        self._freq_options = (101.9e6, 104.4e6, 433.5e6, )
        # Create the labels list
        self._freq_labels = ('101.9e6', '104.4e6', '433.5e6', )
        # Create the combo box
        self._freq_tool_bar = Qt.QToolBar(self)
        self._freq_tool_bar.addWidget(Qt.QLabel('freq' + ": "))
        self._freq_combo_box = Qt.QComboBox()
        self._freq_tool_bar.addWidget(self._freq_combo_box)
        for _label in self._freq_labels: self._freq_combo_box.addItem(_label)
        self._freq_callback = lambda i: Qt.QMetaObject.invokeMethod(self._freq_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._freq_options.index(i)))
        self._freq_callback(self.freq)
        self._freq_combo_box.currentIndexChanged.connect(
            lambda i: self.set_freq(self._freq_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._freq_tool_bar)
        self._volume_range = Range(-1, 10, 0.1, 1, 200)
        self._volume_win = RangeWidget(self._volume_range, self.set_volume, 'volume', "counter_slider", float)
        self.top_grid_layout.addWidget(self._volume_win)
        self._transition_range = Range(0, 10000000, 100, 1000000, 200)
        self._transition_win = RangeWidget(self._transition_range, self.set_transition, 'transition', "counter_slider", float)
        self.top_grid_layout.addWidget(self._transition_win)
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + 'rtl_tcp=10.10.10.10:1234'
        )
        self.rtlsdr_source_0.set_time_now(osmosdr.time_spec_t(time.time()), osmosdr.ALL_MBOARDS)
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(20, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
        self._quadrature_range = Range(0, 1000000, 1000, 500000, 200)
        self._quadrature_win = RangeWidget(self._quadrature_range, self.set_quadrature, 'quadrature', "counter_slider", float)
        self.top_grid_layout.addWidget(self._quadrature_win)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                6000,
                2000,
                firdes.WIN_HAMMING,
                6.76))
        self._cutoff_range = Range(0, 1000000, 1000, 100000, 200)
        self._cutoff_win = RangeWidget(self._cutoff_range, self.set_cutoff, 'cutoff', "counter_slider", float)
        self.top_grid_layout.addWidget(self._cutoff_win)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(1)
        self.audio_sink_0 = audio.sink(48000, '', True)
        self._audio_dec_range = Range(1, 100, 1, 10, 200)
        self._audio_dec_win = RangeWidget(self._audio_dec_range, self.set_audio_dec, 'audio_dec', "counter_slider", float)
        self.top_grid_layout.addWidget(self._audio_dec_win)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(-50, 1)
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=24000,
        	quad_rate=2064000,
        	tau=75e-6,
        	max_dev=5e3,
          )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_rx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.analog_nbfm_rx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_simple_squelch_cc_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.low_pass_filter_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "rtl_uhc_mono")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume

    def get_transition(self):
        return self.transition

    def set_transition(self, transition):
        self.transition = transition

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 6000, 2000, firdes.WIN_HAMMING, 6.76))
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_quadrature(self):
        return self.quadrature

    def set_quadrature(self, quadrature):
        self.quadrature = quadrature

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self._freq_callback(self.freq)
        self.rtlsdr_source_0.set_center_freq(self.freq, 0)

    def get_cutoff(self):
        return self.cutoff

    def set_cutoff(self, cutoff):
        self.cutoff = cutoff

    def get_audio_dec(self):
        return self.audio_dec

    def set_audio_dec(self, audio_dec):
        self.audio_dec = audio_dec





def main(top_block_cls=rtl_uhc_mono, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
