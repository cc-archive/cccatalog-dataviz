import React, { useState } from 'react';
import { ReactComponent as SearchIcon } from '../assets/icons/search.svg';


function SearchFilterBox(props) {
    const [dropdownIsOpen, setDropdownIsOpen] = useState(false);
    const [name, setName] = useState('');
    const [distance, setDistance] = useState('');
    return (
        <div className="searchbar-main-wrapper">
            <div className="title-main">
                Linked Commons
                </div>
            <ul className="searchbar-items-wrapper">

                <li className='searchbar-item'>
                    <button className='searchbar-icon' onClick={() => setDropdownIsOpen(!dropdownIsOpen)}>{<SearchIcon />}</button>
                    {dropdownIsOpen && <DropdownMenu
                        handleSubmit={props.handleSubmit}
                        name={name}
                        setName={setName}
                        distance={distance}
                        setDistance={setDistance} />}
                </li>
            </ul>
        </div>
    );
}

// searchbar and distance
function DropdownMenu(props) {
    const { name, setName, distance, setDistance } = props;
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