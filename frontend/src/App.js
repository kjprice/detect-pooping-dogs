import React, {Component} from 'react';
import axios from 'axios';
import './App.css';

const URL = '/newImage'

const saveImageThrottleTime = 6000; // Wait six seconds before sending another image

function getVideoDevices() {
  return navigator.mediaDevices.enumerateDevices()
  .then((deviceInfos) => {
    return deviceInfos.filter(deviceInfo => deviceInfo.kind === 'videoinput')
  })
}

function getStream(device) {
  const { deviceId } = device;

  // TODO: Set HD video size
  const constraints = {
    video: {
      deviceId: {exact: deviceId},
      width: {ideal: 1280}, height: {ideal: 720}
    }
  };
  return navigator.mediaDevices.getUserMedia(constraints)
  .catch(e => console.error(e))
}

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      canSendImage: true,
      devices: [],
      selectedDevice: null,
      countOfTimesDevicesFetched: 0
    };
  }

  componentDidMount() {
    this.requestDeviceInfos();
  }

  componentDidUpdate = () => {
    this.trySetCanvasDimensions();
  }

  requestDeviceInfos = () => {
    const { countOfTimesDevicesFetched} = this.state;
    if (countOfTimesDevicesFetched >= 2) {
      return;
    }
    getVideoDevices().then(devices => {
      const selectedDevice = devices[0];
      this.setState({
        devices,
        selectedDevice,
        countOfTimesDevicesFetched: countOfTimesDevicesFetched +1
      });
      this.changeDeviceStream(selectedDevice)
    });
  }

  changeDeviceStream = (device) => {
    const { selectedDevice } = this.state;

    getStream(device).then(stream => {
      if (!selectedDevice || !selectedDevice.deviceId) {
        this.requestDeviceInfos();
        return;
      }
      this.video.srcObject = stream;
    })
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

    this.setTimerForImageThrottle();
    axios.post(URL, fd, config).then(response => {
      console.log({response})
    }).catch(error => {
      console.log('error', error)
    })
  }

  drawFrame = () => {
    this.ctx.drawImage(this.video, 0, 0);

    this.canvas.toBlob(this.saveFrame, 'image/jpeg');
  }

  setVideoMainRef = (video) => {
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

    const widthTheSame = this.canvas.width === this.video.videoWidth;
    const heightTheSame = this.canvas.height === this.video.videoHeight;

    if (widthTheSame && heightTheSame) {
      return;
    }

    this.canvas.width = this.video.videoWidth;
    this.canvas.height = this.video.videoHeight;
  }

  videoSelectionChange = (e) => {
    const { devices } = this.state;
    const selectedDevice = devices.find((device) => device.deviceId === e.target.value);
    this.setState({
      selectedDevice
    })
    
    this.changeDeviceStream(selectedDevice);
  }

  renderVideoOption = (device) => {
    return <option key={device.deviceId} value={device.deviceId}>{device.label}</option>
  }

  renderVideoDropDown = () => {
    const { devices, selectedDevice } = this.state;
    if (!devices || selectedDevice == null) {
      return null;
    }

    // Need to have at least two devices to give user a choice
    if (devices.length <= 1) {
      return null;
    }

    return (
      <select value={selectedDevice.deviceId} onChange={this.videoSelectionChange}>
        {devices.map(this.renderVideoOption)}
      </select>
    )
  }
  
  render() {
    return (
      <div className="App">
        {this.renderVideoDropDown()}
        <video ref={this.setVideoMainRef} autoPlay loop muted playsInline></video>
        <canvas ref={this.setCanvasRef} />
      </div>
    );
  }
}

export default App;
