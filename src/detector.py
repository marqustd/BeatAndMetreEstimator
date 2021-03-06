import common
import tempoMetreDetector as tmd
import song
import argparse
import settings

from tempo import combFilterTempoDetector, convolveTempoDetector

from metre import combFilterMetreDetector, convolveNormalizedMetreDetector, combFilterNormalizedMetreDetector, \
    convolveMetreDetector, correlateNormalizedMetreDetector


def prepare_parser():
    tempoDetectorHelp = "tempo detector method. \n Possible detectors: " \
                        "\n combFilterTempoDetector, " \
                        "\n convolveTempoDetector " \
                        "\n (default: combFilterTempoDetector) "

    metreDetectorHelp = "metre detector method. \n Possible detectors: " \
                        "\n combFilterMetreDetector, " \
                        "\n combFilterNormalizedMetreDetector, " \
                        "\n convolveMetreDetector , " \
                        "\n convolveNormalizedMetreDetector, " \
                        "\n correlateNormalizedMetreDetector " \
                        "\n(default: combFilterMetreDetector)"

    tempoParser = argparse.ArgumentParser(add_help=False)
    tempoParser.add_argument("-t", help=tempoDetectorHelp, dest='tempoDetector', default='combFilterTempoDetector')

    metreParser = argparse.ArgumentParser(add_help=False)
    metreParser.add_argument("-m", help=metreDetectorHelp, dest='metreDetector', default='combFilterMetreDetector')

    parser = argparse.ArgumentParser(parents=[tempoParser, metreParser])
    parser.add_argument("song", help="path to song")
    parser.add_argument('--plots', dest='showPlots', default=False,
                        help='show plots (default: disabled)', action='store_const', const=True)
    parser.add_argument('--settings', dest='showSettings', default=False,
                        help='show used settings at the end of program (default: disabled)', action='store_const',
                        const=True)
    parser.add_argument("-p", help='Comb fiter pulses (default: 10)', dest='pulses', default=10, type=int)
    parser.add_argument("-r", help='Resampling ratio. 0 turns off resampling. (default: 4)', dest='resampleRatio',
                        default=4, type=int)
    return parser


def parse_tempo_detector(detector: str):
    if detector == 'combFilterTempoDetector':
        return combFilterTempoDetector.CombFilterTempoDetector()
    elif detector == 'convolveTempoDetector':
        return convolveTempoDetector.ConvolveTempoDetector()
    else:
        return None


def parse_metre_detector(detector: str):
    if detector == 'combFilterMetreDetector':
        return combFilterMetreDetector.CombFilterMetreDetector()
    elif detector == 'combFilterNormalizedMetreDetector':
        return combFilterNormalizedMetreDetector.CombFilterNormalizedMetreDetector()
    elif detector == 'convolveMetreDetector':
        return convolveMetreDetector.ConvolveMetreDetector()
    elif detector == 'convolveNormalizedMetreDetector':
        return convolveNormalizedMetreDetector.ConvolveNormalizedMetreDetector()
    elif detector == 'correlateNormalizedMetreDetector':
        return correlateNormalizedMetreDetector.CorrelateNormalizedMetreDetector()
    else:
        return None


def parse_resample_ratio(resampleRatio, parser):
    if resampleRatio < 0:
        parser.error("Resample ratio has to be positive or zero!")
    elif resampleRatio == 0:
        settings.resampleSignal = False
    else:
        settings.resampleRatio = resampleRatio


def parse_show_plots(showPlots):
    if not showPlots:
        settings.drawMetreFftPlots = False
        settings.drawMetreFilterPlots = False
        settings.drawTempoFftPlots = False
        settings.drawTempoFilterPlots = False
        settings.drawPlots = False
        settings.drawSongBpmEnergyPlot = True
    else:
        settings.drawMetreFftPlots = False
        settings.drawMetreFilterPlots = True
        settings.drawTempoFftPlots = False
        settings.drawTempoFilterPlots = False
        settings.drawPlots = True
        settings.drawSongBpmEnergyPlot = True


parser = prepare_parser()
args = parser.parse_args()
metreDetector = parse_metre_detector(args.metreDetector)
if metreDetector is None:
    parser.error("Wrong metreDetector provided")
tempoDetector = parse_tempo_detector(args.tempoDetector)
if tempoDetector is None:
    parser.error("Wrong tempoDetector provided")
parse_show_plots(args.showPlots)
parse_resample_ratio(args.resampleRatio, parser)
if args.pulses >= 0:
    settings.combFilterPulses = args.pulses
else:
    parser.error("Pulses amount has to be positive!")
detector = tmd.TempoMetreDetector(tempoDetector, metreDetector)
song = song.Song(args.song)
tempo, metre, time = detector.detect_tempo_metre(song)
print()
print("Song tempo: ", tempo)
print("Song metre: ", metre)
if args.showSettings:
    print()
    print(common.prepare_settings_string(tempoDetector, metreDetector))
