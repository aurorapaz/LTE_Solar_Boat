Stream = require('node-rtsp-stream')
stream = new Stream({
name: 'name',
      // streamUrl: 'rtsp://192.168.2.37:80/live/stream',
      streamUrl: 'rtsp://localhost:1234/live/stream',
      wsPort: 9999,
      ffmpegOptions: { // options ffmpeg flags
           '-stats': '', // an option with no neccessary value uses a blank string
           '-r': 30, // options with required values specify the value after the key
      }
})
