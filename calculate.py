import librosa
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from scipy.spatial import distance
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import jaccard_score
from scipy.spatial import distance
from torch import tensor
from sklearn.svm import SVC
from sklearn import svm
import os
from pydub import AudioSegment



def find_audio(url):
    allowed_extensions = ['.mp3', '.ogg', '.flac', '.m4a', '.wav']
    for file in os.listdir(url):
        if any(file.endswith(ext) for ext in allowed_extensions):
            #old_audio = AudioSegment.from_file(os.path.join(url, file))
            old_audio = url+file
            if(old_audio.endswith('.mp3')):
                audio = AudioSegment.from_mp3(old_audio)
                wav_file = os.path.splitext(old_audio)[0] + '.wav'
                audio.export(wav_file, format='wav')
                new_audio = wav_file
            else:
                new_audio = old_audio

            return new_audio
            



def DataExtract(url, col_names):
    tmp = []
    tmp.append(url)

    audio, sr = librosa.load(find_audio(url), dtype = np.float64)
    with open("time.txt", "r") as file:
        start = int(file.readline())
        end = int(file.readline())
    print(start)
    print(end)
    audio = audio[22050*start:22050*end]

    chroma_stft = librosa.feature.chroma_stft(y=audio, hop_length = 512)
    tmp.append(chroma_stft.mean())
    tmp.append(chroma_stft.var())

    RMSEn= librosa.feature.rms(y=audio)
    tmp.append(RMSEn.mean())
    tmp.append(RMSEn.var())

    spec_cent = librosa.feature.spectral_centroid(y=audio)
    tmp.append(spec_cent.mean())
    tmp.append(spec_cent.var())

    spectral_bandwidth = spec_band=librosa.feature.spectral_bandwidth(y=audio,sr=sr)
    tmp.append(spectral_bandwidth.mean())
    tmp.append(spectral_bandwidth.var())

    spec_roll=librosa.feature.spectral_rolloff(y=audio,sr=sr)
    tmp.append(spec_roll.mean())
    tmp.append(spec_roll.var())

    zero_crossing=librosa.feature.zero_crossing_rate(y=audio)
    tmp.append(zero_crossing.mean())
    tmp.append(zero_crossing.var())

    harmony, perceptr = librosa.effects.hpss(y=audio, hop_length=512)
    tmp.append(harmony.mean())
    tmp.append(harmony.var())
    tmp.append(perceptr.mean())
    tmp.append(perceptr.var())

    tempo, _ = librosa.beat.beat_track(y=audio)
    tmp.append(tempo[0])

    mfcc=librosa.feature.mfcc(y=audio, norm = 'ortho')
    for i in range(len(mfcc)):
        tmp.append(mfcc[i].mean())
        tmp.append(mfcc[i].var())


    tmp = np.array(tmp)
    df = pd.DataFrame(tmp.reshape(1,-1), columns = col_names)
    return df



def TakeGenre(all_data, label):
    new_data = all_data.loc[all_data['label'] == label]
    return new_data


def CosineSimilarity(x, genre_data, m):
    x=list(x.iloc[0])
    dist=[]
    rows, cols = (3, 2)
    rec = [[0, 0], [0, 0], [0, 0]]
    match m:
        case 1:
            for i, row in genre_data.iterrows():
                y_cur=list(row)
                cos_sim = cosine_similarity([x], [y_cur])
                dist.append(cos_sim[0][0])
            dist.sort(reverse=True)
            # print(dist)
            for i, row in genre_data.iterrows():
                y_cur=list(row)
                if cosine_similarity([x], [y_cur])==dist[0]:
                    rec[0][0]='index - ' + str(i)
                    rec[0][1]=dist[0]
                elif  cosine_similarity([x], [y_cur])==dist[1]:
                    rec[1][1]=dist[1]
                    rec[1][0]='index - ' + str(i)
                elif cosine_similarity([x], [y_cur])==dist[2]:
                    rec[2][1]=dist[2]
                    rec[2][0]='index - ' + str(i)
            return rec

def ch_name(x):
    if x<10:
        ans = '0000'+str(x)
    else:
        ans = '000'+str(x)
    return ans


def calc_function():
    #---------------------------------------------DATA   PART--------------------------------------------------#
    data = pd.read_csv('Data/new_split/data_3_85.csv', delimiter=',', decimal='.')
    data_for_TakeGenre = pd.read_csv('Data/new_split/data_30_85.csv', delimiter=',', decimal='.')

    data_for_TakeGenre = data_for_TakeGenre.drop(['length'], axis = 1)
    data = data.drop(['length', 'filename'], axis=1)
    data_label = data['label']

    scaler = StandardScaler()
    scaler.fit(data.drop(['label'], axis = 1))
    scaled_data = pd.DataFrame(scaler.transform(data.drop(['label'], axis = 1)), columns = data.drop(['label'], axis = 1).columns)
    train_data = pd.concat([scaled_data, data_label], axis = 1)

    x_train_d3, x_test_d3, y_train_d3, y_test_d3 = train_test_split(train_data.drop(['label'], axis = 1), train_data['label'], test_size=0.2, random_state=24, stratify=train_data['label'])
    #-----------------------------------------------------------------------------------------------------------#



    #----------------------------------------------NEW EXAMPLE-------------------------------------------------#
    sample_columns = data_for_TakeGenre.drop(['label'], axis = 1).columns
    data_extr = DataExtract('upload/', sample_columns)
    ex_data = pd.DataFrame(scaler.transform(data_extr.drop(['filename'], axis=1)), columns = data_extr.drop(['filename'], axis = 1).columns)
    #-----------------------------------------------------------------------------------------------------------#



    #----------------------------------------------DEFINE SVM---------------------------------------------------#
    model_svm = SVC(C = 44.46628955475442, kernel = 'rbf', gamma = 0.01, shrinking = True)
    model_svm.fit(x_train_d3, y_train_d3)
    #-----------------------------------------------------------------------------------------------------------#



    #----------------------------------------------WORK PLACE---------------------------------------------------#
    new_label = model_svm.predict(ex_data)[0]

    g_data = TakeGenre(data_for_TakeGenre, new_label)

    smth = CosineSimilarity(ex_data, g_data.drop(['filename', 'label'], axis = 1), 1)

    genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
    genre = genres[new_label]

    a1 = ch_name(int(smth[0][0].split(' - ')[1])%85)
    a2 = smth[0][1]

    b1 = ch_name(int(smth[1][0].split(' - ')[1])%85)
    b2 = smth[1][1]

    c1 = ch_name(int(smth[2][0].split(' - ')[1])%85)
    c2 = smth[2][1]

    with open("similar.txt", "w") as file:
        file.write(genre)
        file.write('\n')

        file.write('Data/genres_85/'+ genre + '/'+genre+'.'+a1+'.wav')
        file.write('\n')
        file.write(str(a2))
        file.write('\n')

        file.write('Data/genres_85/'+ genre + '/'+genre+'.'+b1+'.wav')
        file.write('\n')
        file.write(str(b2))
        file.write('\n')

        file.write('Data/genres_85/'+ genre + '/'+genre+'.'+c1+'.wav')
        file.write('\n')
        file.write(str(c2))
        file.write('\n')