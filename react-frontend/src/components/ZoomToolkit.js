import React from 'react';
import Plus from '../assets/zoomtoolkit/plus.svg'
import Minus from '../assets/zoomtoolkit/minus.svg'


class ZoomToolkit extends React.Component {
    render() {
        return (
            <div className="zoomtoolkit-wrapper">
            <button className="plus-button" onClick = {this.props.handleZoomIn}><img src={Plus} alt="plus" /></button>
            <button className="minus-button" onClick= {this.props.handleZoomOut}><img src={Minus} alt="minus" /></button>
          </div>
        );
    }
}

export default ZoomToolkit;