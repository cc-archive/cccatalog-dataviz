import React from 'react';
import ReactHighcharts from 'react-highcharts';
import Exporting from 'highcharts/modules/exporting';
import highcharts from 'highcharts';
Exporting(ReactHighcharts.Highcharts);


class LicenseChart extends React.Component {
    render() {
        let { node } = this.props;
        console.log("NEW:", node);
        return (
            <React.Fragment>
                <div id="licensechart">
                    <div className="licensechart-modal-content" >
                        <div id="licensechart-data-main">
                            {node.provider_domain === 'Domain not available' ? <div><span>The CC License information of</span><b> {node.id} </b><span>is not available</span></div> : this.getPieChart()}
                        </div>
                        <div className="licensechart-modal-footer" style={{ textAlign: 'right', margin: '10px' }}>
                            <button type="button" id="closeBtn" onClick={this.props.handler}>Close</button>
                        </div>
                    </div>
                </div>
            </React.Fragment>
        )
    }

    shouldComponentUpdate(props){
        if(this.props.node === props.node){
            return false;
        }
        return true;
    }
    getPieChart() {
        // assumes that node has provider_domain
        let node = this.props.node;
        let data = node.cc_licenses;
        let licensed_data = []
        for (let license in data) {
            //build a dictionary with license as key and as value, the number of licenses
            let element = {}
            element.name = this.beautifyLicensename(license.substring(1, license.length - 1));
            element.y = data[license];
            //push that dictionary to a list
            licensed_data.push(element)
        }

        let config = {
            exporting: {
                showTable: false,
                tableCaption: '<br><b>Data table</b>',
            },
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: `Use of CC licenses by<br> <b> ${node.provider_domain} </b>`
            },
            subtitle: {
                text: `Total links to Creative Commons: <b> ${node.licenses_qty} </b><br>Images on this domain: <b> ${node.images} </b>`
            },
            tooltip: {
                pointFormat: '{series.name}: {point.percentage:.2f}%'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.2f} %',
                        style: {
                            color: (highcharts.theme && highcharts.theme.contrastTextColor) || 'black'
                        }
                    }
                }
            },
            series: [{
                name: 'License',
                colorByPoint: true,
                data: licensed_data
            }]
        };
        return <ReactHighcharts config={config}></ReactHighcharts>;
    }

    // helper function to beautify license name of the particular node
    beautifyLicensename(string) {
        let no_comma = string.replace(",", " v.");
        let no_apostrophe = no_comma.replace(/'+/g, "");
        let final_name;
        if (no_apostrophe.substring(0, 2) === "by") {
            final_name = "cc " + no_apostrophe;
        } else {
            final_name = no_apostrophe;
        }
        return final_name;
    }
}


export default LicenseChart;