clean:
	rm -rf build

build-FFmpegLayer: clean
	mkdir -p "$(ARTIFACTS_DIR)/bin"
	mkdir build
	cd build && curl https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar xJ
	mv build/ffmpeg*/ffmpeg build/ffmpeg*/ffprobe $(ARTIFACTS_DIR)/bin
