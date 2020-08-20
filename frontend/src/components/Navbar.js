import React, { Component } from 'react';
import { ReactComponent as LightLogo } from '../assets/logo/light-logo.svg';
import { ReactComponent as DarkLogo } from '../assets/logo/dark-logo.svg';

class Navbar extends Component {
    render() {
        return (
            <div className='navbar-wrapper'>
                <div className='cc-logo'>
                    {this.props.isDarkMode ? <DarkLogo /> : <LightLogo />}
                </div>
                <a className='explore-cc-btn' href='https://creativecommons.org/' target='__blank'>
                    Explore CC
                </a>
            </div>
        )
    }
}


export default Navbar;
