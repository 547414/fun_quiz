class PCMStreamProcessor extends AudioWorkletProcessor {
  constructor() {
    super()
    this.buffer = []
    this.ptr = 0
    this.playing = false

    this.port.onmessage = (e) => {
      if (e.data.reset) {
        this.buffer = []
        this.ptr = 0
        this.playing = true
      } else if (e.data.done) {
        this.playing = false
      } else if (e.data.audio) {
        this.buffer.push(...e.data.audio)
      }
    }
  }

  process(_, outputs) {
    const out = outputs[0][0]
    for (let i = 0; i < out.length; i++) {
      out[i] = this.ptr < this.buffer.length ? this.buffer[this.ptr++] : 0
    }
    return true
  }
}

registerProcessor('pcm-stream-processor', PCMStreamProcessor)
