import React, {Component} from 'react';
import {ReactComponent as LightLogo }  from '../assets/logo/light-logo.svg';
import {ReactComponent as DarkLogo} from '../assets/logo/dark-logo.svg';


class Sidebar extends Component{

    render(){
        return (
            <div className='sidebar-wrapper'>
                <div className='cc-logo'>
                    {this.props.isDarkMode ? <DarkLogo/> :<LightLogo />}
                </div>
                <div className='project-info'>
                    <div className='project-heading'>The linked commons</div>
                    <div className='project-desc'>This graph visualizes the relationships between domains that use Creative Commons licenses. For more information see our <a href='https://github.com/creativecommons/cccatalog-dataviz/' target='__blank'>Github repo</a>.</div>
                </div>
            </div>
        )
    }
}


export default Sidebar;