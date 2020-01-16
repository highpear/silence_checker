import sys, glob
from pydub import AudioSegment
import matplotlib.pyplot as plt

# 波形グラフの表示
def show_graph(sound):
    samples = sound.get_array_of_samples()
    plt.plot(samples)
    plt.show()

def main():

    # デフォルト値
    TARGET_DIR = './' # デフォルトでカレントを対象
    DEFAULT_SEC = 5.0 # デフォルトで5秒間の無音を調べる
    audio_source_files = [] # ディレクトリに存在するm4aファイルを取得
    error_files = [] # エラーファイル（無音あり）

    # コマンドライン引数処理
    # -d [指定ディレクトリ] -s [無音の秒数]
    args = sys.argv
    for i, val in enumerate(args):
        if val == '-d':
            TARGET_DIR = args[i+1]
        elif val == '-s':
            DEFAULT_SEC = float(args[i+1])
        else:
            continue

    # 全m4aファイルを取得
    audio_source_files = glob.glob(TARGET_DIR + '*.m4a')

    if len(audio_source_files) == 0:
        print('No Compatible Audio File in {}'.format(TARGET_DIR))
        sys.exit()

    # 全オーディオファイルに以下を適用
    for name in audio_source_files:

        sound = AudioSegment.from_file(name, 'm4a')
        sound_array = sound.get_array_of_samples()
        fps  = sound.frame_rate
        ch = sound.channels

        # print('フレームレート:', fps)
        # print('チャネル:', ch)

        zeros = 0
        # sound_arrayの要素はチャネル分だけ倍
        for n in sound_array:
            if(n == 0): # 無音
                zeros += 1
                # 指定した時間だけ無音が続いた時点でループを抜ける
                if zeros >= fps * DEFAULT_SEC * ch:
                    error_files.append(name)
                    break

    # 結果表示
    print('About ' + str(DEFAULT_SEC) + ' sec. silence')
    if len(error_files) > 0: # エラーファイル（無音）が存在
        print('Error Files:')
        for i, name in enumerate(error_files):
            print('No.' + str(i+1), ':', name)
    else: print('No Error!') # エラーなし

if __name__ == "__main__":
    main()