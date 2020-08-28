import React from 'react';
import { ReactComponent as Plus } from '../assets/zoomtoolkit/plus.svg'
import { ReactComponent as Minus } from '../assets/zoomtoolkit/minus.svg'
import { ReactComponent as MapPin } from '../assets/zoomtoolkit/map-pin.svg'

class ZoomToolkit extends React.Component {
    render() {
        return (
            <div className="zoomtoolkit-wrapper">
                <button className="plus-button" onClick={this.props.resetZoom}><MapPin /></button>
                <button className="plus-button" onClick={this.props.handleZoomIn}><Plus /></button>
                <button className="minus-button" onClick={this.props.handleZoomOut}><Minus /></button>
            </div>
        );
    }
}

export default ZoomToolkit;

