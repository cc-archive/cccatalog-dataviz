import React, { useState } from 'react';
import { ReactComponent as SearchIcon } from '../assets/icons/search.svg';


class SearchFilterBox extends React.Component {
    state= {
        dropdownIsOpen:false,
    }
    render() {
        return (
            <div className="searchbar-main-wrapper">
                <div className="title-main">
                    Linked Commons
                </div>
                <ul className="searchbar-items-wrapper">

                    <li className='searchbar-item'>
                        <a className='searchbar-icon' href='javascript:void(0)' onClick={() => this.setState({dropdownIsOpen: !this.state.dropdownIsOpen})}>{<SearchIcon />}</a>
                        {this.state.dropdownIsOpen && <DropdownMenu handleSubmit={this.props.handleSubmit} />}
                    </li>
                </ul>
            </div>
        );
    }
}

// searchbar and distance
function DropdownMenu(props) {
    const [name, setName] = useState('');
    const [distance, setDistance] = useState('');
    return (
        <div className='dropdown-wrapper'>
            <form onSubmit={(e) => { e.preventDefault(); props.handleSubmit({ name, distance }) }}>
                <div className='dropdown-menu-item'>
                    <label htmlFor='graphNodeName'><span className='searchbar-icon'>{<SearchIcon />}</span>Name</label>
                    <input type='text' id='graphNodeName' onChange={(e) => setName(e.target.value)} placeholder='icij' value={name} />
                </div>
                <div className={`dropdown-menu-item ${name === '' ? 'disabled' : ''}`}>
                    <label htmlFor='nodeDistance'><span className='searchbar-icon'>{<SearchIcon />}</span>Distance</label>
                    <input type='number' id='nodeDistance' disabled={name === ''} onChange={(e) => setDistance(e.target.value)} value={distance} placeholder='5' />
                </div>
                <div className={`dropdown-menu-item ${name === '' || distance === '' ? 'disabled' : ''}`}>
                    <button disabled={name === '' || distance === ''}>Filter Graph</button>
                </div>
            </form>

        </div>
    )
}

export default SearchFilterBox;