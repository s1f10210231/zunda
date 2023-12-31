import os
import subprocess
def mk_movieList(movie_folder):
    files = os.listdir(movie_folder)
    files = [x for x in files if x[-4:] == '.mp4']  ### x[-4]'後ろ4文字目以降'
    files = [x for x in files if x[0] != '.']
    return files

def mk_starts_ends(wk_dir, movie):
    os.chdir(wk_dir)
    output = subprocess.run(["ffmpeg", "-i", movie, "-af", "silencedetect=noise=-33dB:d=0.6", "-f", "null", "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(output)
    s = str(output)
    lines = s.split('\\n')
    time_list =[]
    for line in lines:
        if "silencedetect" in line:
            words = line.split(" ")
            for i in range(len(words)):
                if "silence_start" in words[i]:
                    time_list.append(float(words[i+1]))
                if "silence_end" in words[i]:
                    time_list.append(float(words[i+1]))
    print(time_list)
    starts_ends = list(zip(*[iter(time_list)]*2))
    return starts_ends

def mk_jumpcut(wk_dir, movie, starts_ends):
    os.chdir(wk_dir)
    for i in range(len(starts_ends)-1):
        movie_name = movie.split(".") 
        splitfile = "./JumpCut/" + movie_name[0] + "_" + str(i) + ".mp4"
        print(splitfile)
        output = subprocess.run(["ffmpeg", "-i", movie, "-ss", str(starts_ends[i][1]), "-t", str(starts_ends[i+1][0]-starts_ends[i][1]), splitfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


movie_folder = os.path.abspath(f"./onnxruntime-linux-x64-1.13.1/generate")

os.chdir(movie_folder)
wk_dir = os.path.abspath(".")
try:
    os.mkdir("JumpCut")
except:
    pass

movie_list = mk_movieList(movie_folder)

for movie in movie_list:
    print(movie)
    starts_ends = mk_starts_ends(wk_dir, movie)
    print(starts_ends)
    mk_jumpcut(wk_dir, movie, starts_ends)
