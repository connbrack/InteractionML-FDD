<script>
// Imports
import chart from '$lib/highcharts';
import Highcharts from 'highcharts';
import {
    Button,
    Dropdown,
    DropdownItem,
    Spinner,
    Toggle,
    Modal,
    Label,
    Textarea,
    Radio,
} from 'flowbite-svelte';

import {
    Icon,
} from 'flowbite-svelte-icons';

import {
    onMount
} from 'svelte'

import {
    serverIP
} from '$lib/localstore.js';

// ------------------------ Page initialization -----------------------------
onMount(async () => {
    getAHUsensors();
    await getSensorData();
    updateGraph()
});

// ------------------------ UI elements -----------------------------
let DropdownIsOpen = false;
let graphModeSelect = false;
let showPopup = false;
let showDataLabelForm = false;
let textareaprops = {};
let selectedOption = '';
let notes = '';

const dropdownClick = async (sensor) => {
    currentSensor = sensor;
    closeDropdown();
    await getSensorData();
    updateGraph();
}
const closeDropdown = () => {
    DropdownIsOpen = false;
};

const labelDataButton = async () => {
    if (selectedData == undefined) {
        showPopup = true;
        setTimeout(() => {
            showPopup = false;
        }, 5000);
    } else {
        showDataLabelForm = true;
    }
};

const submitDataButton = async (event) => {
    event.preventDefault();
    await submitDataLabel();

    // Clear form 
    showDataLabelForm = false;
    selectedOption = '';
    notes = '';
    config.xAxis.plotBands = [];
}

// ------------------------ API functions ------------------------------

let currentSensor = "MA_TEMP";
let sensorData = [];
let AHUsensors = [];

const getAHUsensors = async () => {
    const response = await fetch(`${serverIP}/AHU_sensor_info`)
    const data = await response.json();
    AHUsensors = data;
}
const getSensorData = async () => {
    const response = await fetch(`${serverIP}/sensor_data?sensor=${currentSensor}`)
    const data = await response.json();
    sensorData = data;
}

const submitDataLabel = async () => {
    const response = await fetch(`${serverIP}/apply_data_label`, {
        method: 'POST',
        body: JSON.stringify({
            option: selectedOption,
            notes: notes,
            selectedData: selectedData
        })
    })
    const result = await response.json();
}

// ------------------------ Graph ------------------------------

let selectedData = undefined;
let config = {
    chart: {
        type: "line",
        zoomType: 'x',
        panning: true,
        panKey: 'shift',
        zooming: {
            mouseWheel: {
                enabled: true,
                sensitivity: 1.1,
                type: 'x'
            }
        }
    },
    title: {
        text: 'Title',
    },
    subtitle: {
        text: 'Sensor label: '
    },
    xAxis: {
        type: 'datetime',
    },
    series: [{
        allowPointSelect: true,
        color: '#7E22CE'

    }],
    legend: {
        enabled: false
    },
    credits: {
        enabled: false
    },

};

// ------------------------ Graph click functions -----------

function selectPointsByDrag(e) {
    selectedData = [e.xAxis[0].min, e.xAxis[0].max];
    config.series[0].zoneAxis = 'x';
    config.xAxis.plotBands = [{
        from: e.xAxis[0].min,
        to: e.xAxis[0].max,
        color: 'rgba(69, 167, 255, 0.5)'
    }, ]

    return false;
}

function unselectByClick() {
    selectedData = undefined;
    config.series[0].zoneAxis = [];
    config.xAxis.plotBands = [];
}

// ------------------------ Graph UI changes -----------
function updateGraph() {
    config.series[0] = {
        data: sensorData['data'],
        name: sensorData['name']
    };
    config.title.text = `${sensorData['name']}`;
    config.subtitle.text = `Sensor label: ${sensorData['label']}`;
    config.yAxis = {
        title: {
            text: `${sensorData['name']} (${sensorData['unit']})`
        }
    };
};

function selectDataClick() {
    if (graphModeSelect == false) {
        config.chart.events = {
            selection: selectPointsByDrag,
            // selectedpoints: selectedPoints,
            click: unselectByClick
        };
        graphModeSelect = true;
    } else {
        config.chart.events = {
            selection: undefined,
            selectedpoints: undefined,
            click: undefined
        };
        graphModeSelect = false;
    }
};
</script>

<main>

    {#if sensorData.length === 0}
    <br /><br />
    <br /><br />
    <Spinner size=20 />

    {:else}

    <div class="left-dropdown">
        <Button>Select sensor<Icon name="chevron-down-solid" class="w-2 h-3 ml-2 text-white dark:text-white" /></Button>
        <Dropdown bind:open={DropdownIsOpen} class="overflow-y-auto py-1 h-64 whitespace-nowrap left-0" placement="bottom">
            {#each Object.entries(AHUsensors) as [key, sensorName], index (key)}
            <DropdownItem on:click={() => dropdownClick(sensorName['label'])}>{sensorName['name']}</DropdownItem>
            {/each}
        </Dropdown>
    </div>

    <br /><br />
    <div class="chart" use:chart={config}></div>

    <div class="left-dropdown" style="display: flex; gap: 10px;">
        <Button on:click={() => labelDataButton()}>Set data label</Button>
        <Toggle on:change={() => selectDataClick()}>Toggle data selection mode</Toggle>
        <br /><br />
    </div>

    {/if}

    <!------------------------------- Popup elements ---------------------------------------->
    <Modal bind:open={showDataLabelForm} size="xs" autoclose={false} class="w-full">
        <form class="flex flex-col space-y-6" on:submit={submitDataButton}>
            <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Label Data</h3>
            <Label class="space-y-2">
                Select an option
                <Radio name="example" bind:group={selectedOption} value="Faulty Data">Faulty Data</Radio>
                <Radio name="example" bind:group={selectedOption} value="Unfaulty Data">Unfaulty Data</Radio>
                <Radio name="example" bind:group={selectedOption} value="Remove all labels from selection">Remove all labels from selection</Radio>
            </Label>
            <Label class="space-y-2">
                <span>Notes</span>
                <Textarea {...textareaprops} bind:value={notes} />
            </Label>
            <Button type="submit" class="w-full1">Submit</Button>
        </form>
    </Modal>

    {#if showPopup}
    <div class="popup">
        <p>No data selected</p>
    </div>
    {/if}

</main>

<style>
.left-dropdown {
    text-align: left;
}

.popup {
    position: fixed;
    bottom: 0;
    right: 0;
    background-color: #1F2937;
    /* Red */
    color: #F98080;
    padding: 16px;
    margin: 20px;
    border-radius: 5px;
    z-index: 1000;
    /* Sit on top */
    animation-name: fadein;
    animation-duration: 0.5s;
}

@keyframes fadein {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}
</style>