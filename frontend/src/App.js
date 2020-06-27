import React, {Component} from 'react';
import axios from 'axios';
import './App.css';

const URL = 'http://localhost:5000/newImage'

const saveImageThrottleTime = 1000; // Wait one second before sending another image

function getVideoMedia() {
return navigator.mediaDevices.enumerateDevices()
  .then((deviceInfos) => {
    for (const deviceInfo of deviceInfos) {
      if (deviceInfo.kind === 'videoinput') {
        return deviceInfo;
      }
    }
  })
}

function getStream(device) {
  const { deviceId } = device;

  // TODO: Set HD video size
  const constraints = {
    video: {deviceId: {exact: deviceId} }
  };
  return navigator.mediaDevices.getUserMedia(constraints)
}

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      canSendImage: true
    };
  }
  componentDidMount() {
    getVideoMedia().then(deviceInfo => {
      console.log(deviceInfo);

      return getStream(deviceInfo)
      .then(stream => {
        this.video.srcObject = stream;
      })
    });
  }

  setTimerForImageThrottle = () => {
    setTimeout(() => {
      this.setState({
        canSendImage: true
      })
    }, saveImageThrottleTime);
  }

  saveFrame = (blob) => {
    const { canSendImage } = this.state;
    if (!canSendImage) {
      return;
    }
    
    const fd = new FormData();

    fd.append('fname', 'image.jpg');
    fd.append('image', blob);

    const config = {
      header : {
        'Content-Type' : 'multipart/form-data'
      }
    }

    this.setState({
      canSendImage: false
    });

    axios.post(URL, fd, config).then(response => {
      console.log('response', response);
      this.setTimerForImageThrottle();
    }).catch(error => {
      this.setTimerForImageThrottle();
      console.log('error', error)
    })
  }

  drawFrame = () => {
    this.ctx.drawImage(this.video, 0, 0);

    this.canvas.toBlob(this.saveFrame, 'image/jpeg');
  }

  setVideoRef = (video) => {
    this.video = video;

    video.addEventListener('loadedmetadata', this.trySetCanvasDimensions, false);
    video.addEventListener('timeupdate', this.drawFrame, false);
  }
  
  setCanvasRef = (canvas) => {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
  }

  trySetCanvasDimensions = () => {
    if (!this.canvas || !this.video) {
      return;
    }

    this.canvas.width = this.video.videoWidth;
    this.canvas.height = this.video.videoHeight;
  }
  
  render() {
    return (
      <div className="App">
        <video ref={this.setVideoRef} autoPlay></video>
        <canvas ref={this.setCanvasRef} />
      </div>
    );
  }
}

export default App;
