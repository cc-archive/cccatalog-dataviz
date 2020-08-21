import React, { Component } from 'react';
import { ReactComponent as DarkLogo } from '../assets/logo/light-logo.svg';
import { ReactComponent as LightLogo } from '../assets/logo/dark-logo.svg';
import { ReactComponent as SunIcon } from '../assets/icons/sun.svg';
import { ReactComponent as MoonIcon } from '../assets/icons/moon.svg';

class Navbar extends Component {
    render() {
        return (
            <div className={`navbar-wrapper ${this.props.isLoading===true ? 'loading' : ''}`}>
                <div className='cc-logo'>
                    {(!this.props.isDarkMode || this.props.isLoading===true) ?  <DarkLogo /> : <LightLogo />}
                </div>
                <a className='explore-cc-btn' href='https://creativecommons.org/' target='__blank'>
                    Explore CC
                </a>
                <DarkModeSwitch
                    isDarkMode={this.props.isDarkMode}
                    toggleThemeHandler={this.props.toggleThemeHandler} />
            </div>
        )
    }
}


export default Navbar;



function DarkModeSwitch({ isDarkMode, toggleThemeHandler }) {
    return (
        <div className='darkmodeswitch' onClick={toggleThemeHandler}>
            {isDarkMode ? <SunIcon /> : <MoonIcon />}
        </div>
    )
}