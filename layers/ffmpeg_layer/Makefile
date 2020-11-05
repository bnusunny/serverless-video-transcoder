clean:
	rm -rf build

build-FFmpegLayer: clean
	mkdir -p "$(ARTIFACTS_DIR)/bin"
	mkdir build
	cd build && curl https://awsguru.s3.cn-north-1.amazonaws.com.cn/public/ffmpeg/ffmpeg-release-amd64-static.tar.xz | tar xJ
	mv build/ffmpeg*/ffmpeg build/ffmpeg*/ffprobe $(ARTIFACTS_DIR)/bin
