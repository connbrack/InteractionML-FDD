<script>


    // Imports
	import highcharts from '$lib/highcharts';
    import { Button, Dropdown, DropdownItem ,Spinner } from 'flowbite-svelte';
    import { Icon } from 'flowbite-svelte-icons';
    import { onMount } from 'svelte'
    import { serverIP } from '$lib/localstore.js';

    // Initial values
	let currentSensor  = "MA_TEMP";
    let sensorData = [];
    let AHUsensors = [];
    let isOpen = false;

    // UI elements 
    const dropdownClick = async (sensor) => {
        currentSensor = sensor;
        closeDropdown();
        await getSensorData();
        updateGraph();
    }
    const closeDropdown = () => {
        isOpen = false;
    };

    // API functions
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

    // Page initialization
    onMount(async () => {
        getAHUsensors();
        await getSensorData();
        updateGraph()
    });

    // Graph
    let config = {
        chart: {
            zoomType: 'x',
            panning: true,
            panKey: 'shift',
            mouseWheel: true
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
            type: 'line',
            color: '#BD93F9'

        }],
        legend: {
            enabled: false
        },
        credits: {
            enabled: false
        },

	};
	
	function updateGraph() {
		config.series[0] = {data: sensorData['data'], name: sensorData['name']};
        config.title.text = `${sensorData['name']}`;
        config.subtitle.text = `Sensor label: ${sensorData['label']}`;
		config.yAxis = {title: { text: `${sensorData['name']} (${sensorData['unit']})`}};
	}

</script>


<main>

{#if sensorData.length === 0}
    <br /><br />
    <br /><br />
    <Spinner size=20 />
{:else}


    <div class="left-dropdown">
    <Button>Select sensor<Icon name="chevron-down-solid" class="w-2 h-3 ml-2 text-white dark:text-white" /></Button>
    <Dropdown bind:open={isOpen} class="overflow-y-auto py-1 h-64 whitespace-nowrap left-0" placement="bottom">
        {#each Object.entries(AHUsensors) as [key, sensorName], index (key)}
            <DropdownItem on:click={() => dropdownClick(sensorName['label'])}>{sensorName['name']}</DropdownItem>
        {/each}
    </Dropdown>
    </div>

    <br /><br />
    <div class="chart" use:highcharts={config}></div>

{/if}
</main>

<style>
.left-dropdown {
    text-align: left;
}

</style>