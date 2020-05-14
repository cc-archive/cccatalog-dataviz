import React from 'react';
import { Pie, defaults } from 'react-chartjs-2'


class LicenseChart extends React.Component {

    constructor(props) {
        super(props)
        defaults.global.showLines = true;
        defaults.global.tooltips.mode = 'nearest';
        defaults.global.tooltips.position = 'average';
        defaults.global.tooltips.backgroundColor = 'rgba(255, 255, 255, 0.8)';
        defaults.global.tooltips.displayColors = true;
        defaults.global.tooltips.borderColor = '#c62828';
        defaults.global.tooltips.borderWidth = 1;
        defaults.global.tooltips.titleFontColor = '#000';
        defaults.global.tooltips.bodyFontColor = '#000';
        defaults.global.tooltips.caretPadding = 4;
        defaults.global.tooltips.intersect = false;
        defaults.global.tooltips.mode = 'nearest';
        defaults.global.tooltips.position = 'nearest';
        defaults.global.legend.display = true;
        defaults.global.legend.position = 'bottom';
        defaults.global.hover.intersect = false;
    }


    render() {
        let { node } = this.props;
        return (
            <React.Fragment>
                <div id="licensechart" style={{ display: 'block', border: '1px solid black', position: 'fixed', 'top': '50%', 'left': '50%', 'transform': 'translate(-50%, -50%)', width: '600px', maxWidth: '100%', background: 'white', padding: '20px' }}>
                    <div className="licensechart-modal-content" >
                        <div id="licensechart-data-main">
                            {node.provider_domain==='Domain not available'? `The CC License information of ${node.id} is not available`: this.getPieChart()}
                        </div>
                        <div className="licensechart-modal-footer" style={{ textAlign: 'right', margin: '10px'}}>
                            <button type="button" id="closeBtn" onClick={this.props.handler}>Close</button>
                        </div>
                    </div>
                </div>
            </React.Fragment>
        )
    }


    getPieChart = () => {
        let chartValues = []
        let chartLabels = []
        let data = this.props.node.cc_licenses;
        for (let license in data) {
            chartLabels.push(this.beautifyLicensename(license.substring(1, license.length - 1)));
            chartValues.push(data[license]);
        }
        const chartData = {
            datasets: [
                {
                    data: chartValues,
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56'
                        ],
                        hoverBackgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56'
                        ]
                },
            ],
            labels: chartLabels,
        };
        const chartOptions = {
            events: ['mousemove', 'mouseout', 'touchstart', 'touchmove', 'touchend'],
            layout: {
                padding: {
                    left: 20,
                    right: 20,
                    top: 0,
                    bottom: 10,
                },
            },
            legend: {
                display: true,
            },
            responsive: true,
            maintainAspectRatio: true,
            tooltips: {
                callbacks: {
                    label: function (tooltipItem, data) {
                        const dataset = data.datasets[tooltipItem.datasetIndex];
                        const meta = dataset._meta[Object.keys(dataset._meta)[0]];
                        const total = meta.total;
                        const currentValue = dataset.data[tooltipItem.index];
                        const percentage = parseFloat(
                            ((currentValue / total) * 100).toFixed(3)
                        );
                        return currentValue + ' (' + percentage + '%)';
                    },
                    title: function (tooltipItem, data) {
                        return data.labels[tooltipItem[0].index];
                    },
                },
            },
        };
        return <Pie data={chartData} options={chartOptions} />
    }


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