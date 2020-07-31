import React, { Component } from 'react';
import {
    Combobox,
    ComboboxInput,
    ComboboxPopover,
    ComboboxList,
    ComboboxOption,
} from "@reach/combobox";
import "@reach/combobox/styles.css";


class InputSuggest extends Component {
    constructor() {
        super();
        this.state = {
            // suggestions for the current keyword
            suggestions: [],
            // Implementing a cache to save previous fetched results
            cache: {},
        }
    }

    fetchSuggestions = async (value) => {
        value = value.trim().toLowerCase();
        if (value) {
            if (this.state.cache[value]) {
                this.setState({
                    suggestions: this.state.cache[value]
                });
            } else {
                let res = await fetch(`${this.props.SERVER_BASE_URL}/suggestions/?q=${value}`);
                let jsonData = await res.json();
                if (jsonData['error']) {
                    this.setState({
                        suggestions: [],
                    });
                } else {
                    this.state.cache[value] = jsonData['suggestions'];
                    this.setState({
                        suggestions: jsonData['suggestions']
                    });
                }
            }
        }
    }

    handleChange = (e) => {
        // Update the value
        this.props.setName(e.target.value);
        // Fetch Suggestion
        this.fetchSuggestions(e.target.value);
    }

    render() {
        return (
            <div>
                <Combobox aria-label={this.props.id} onSelect={(e) => { this.props.setName(e) }} >
                    <ComboboxInput
                        id={this.props.id}
                        onChange={this.handleChange}
                        placeholder={this.props.placeholder}
                        value={this.props.value}
                    />
                    {this.state.suggestions && (
                        <ComboboxPopover className="shadow-popup">
                            {this.state.suggestions.length > 0 ? (
                                <ComboboxList>
                                    {this.state.suggestions.map((instance) => {
                                        return <ComboboxOption key={instance.id} value={instance.id} />;
                                    })}
                                </ComboboxList>
                            ) : (
                                    <span style={{ display: "block", margin: 8 }}>
                                        No results found
                                    </span>
                                )}
                        </ComboboxPopover>
                    )}
                </Combobox>
            </div>
        )
    }
}


export default InputSuggest;