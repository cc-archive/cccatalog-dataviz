import React from 'react';

class InfoBox extends React.Component {
    render() {
        return (
            <div className='infoBox'>
                <div style={{ textAlign: "left", margin: '10px' }}>
                    <div style={{ fontWeight: 'bold', marginBottom: '10px' }}>HOVERED EDGE</div>
                    <div>Source: {this.props.linkName ? this.props.linkName.split('_')[0] : null}</div>
                    <div>Destination: {this.props.linkName ? this.props.linkName.split('_')[1] : null}</div>
                </div>
            </div>
        )
    }
}

export default InfoBox;