<script>

  // Imports
  import chart from '$lib/highcharts';
  import Highcharts from 'highcharts';
  import { Button, Dropdown, DropdownItem ,Spinner, Badge } from 'flowbite-svelte';
  import { Toggle, Modal, Label, Input, Textarea, Select } from 'flowbite-svelte';
  import { Icon } from 'flowbite-svelte-icons';
  import { onMount } from 'svelte'
  import { serverIP } from '$lib/localstore.js';

  // Initial values
	let currentSensor  = "MA_TEMP";
  let sensorData = [];
  let AHUsensors = [];
  let DropdownIsOpen = false;
  let graphModeSelect = false; 
  let selectDataButtonLabel = "zoom mode";
  let formModal = false;
  let selected;
  let textareaprops = {
    id: 'message',
    name: 'message',
    label: 'Your message',
    rows: 4,
    placeholder: 'Leave a comment...'
  };
  let faultLabel = [
    { value: 'unfaulty', name: 'This data is un-faulty' },
    { value: 'faulty', name: 'This data is faulty' },
  ];

  // UI elements 
  const dropdownClick = async (sensor) => {
      currentSensor = sensor;
      closeDropdown();
      await getSensorData();
      updateGraph();
  }
  const closeDropdown = () => {
      DropdownIsOpen = false;
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

  function selectPointsByDrag(e) {
    config.series[0].zoneAxis = 'x';
    config.xAxis.plotBands =  [
          {from: e.xAxis[0].min, to: e.xAxis[0].max, color: 'rgba(69, 167, 255, 0.5)'},
    ]

    this.series.forEach(series => {
      series.points.forEach(point => {
        if (point.x >= e.xAxis[0].min && point.x <= e.xAxis[0].max) {
          point.select(true, true);
        }
      });
    });

    // Fire a custom event
    Highcharts.fireEvent(
      this,
      'selectedpoints', {
        points: this.getSelectedPoints()
      }
    );

    return false; // Don't zoom
  }

function toast(chart, text) {
  chart.toast = chart.renderer.label(text, 100, 120)
    .attr({
      fill: Highcharts.getOptions().colors[0],
      padding: 10,
      r: 5,
      zIndex: 8
    })
    .css({ color: '#FFFFFF' })
    .add();

  setTimeout(function() { chart.toast.fadeOut(); }, 2000);
  setTimeout(function() { chart.toast = chart.toast.destroy(); }, 2500);
}
/*
 * The handler for a custom event, fired from selection event
 */
function selectedPoints(e) {
  // Show a label
  toast(
    this,
    `<b>${e.points.length} points selected.</b>
        <br>Click on empty space to deselect.`
  );
}

/*
 * On click, unselect all points
 */
function unselectByClick() {
  config.series[0].zoneAxis = [];
  config.xAxis.plotBands =  [];
  const points = this.getSelectedPoints();
  if (points.length > 0) {
    points.forEach(point => point.select(false));
  }
}

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
	
function updateGraph() {
  config.series[0] = {data: sensorData['data'], name: sensorData['name']};
  config.title.text = `${sensorData['name']}`;
  config.subtitle.text = `Sensor label: ${sensorData['label']}`;
  config.yAxis = {title: { text: `${sensorData['name']} (${sensorData['unit']})`}};
};

function selectDataClick() {
    if (graphModeSelect == false) {
      config.chart.events = {
              selection: selectPointsByDrag,
              selectedpoints: selectedPoints,
              click: unselectByClick
              };
      // config.chart.resetZoomButton.theme.style.display = 'none';
      graphModeSelect = true;
      selectDataButtonLabel = "select mode";
    } else {
      config.chart.events = {
              selection: undefined,
              selectedpoints: undefined,
              click: undefined
              };

      // config.chart.resetZoomButton.theme.style.display = 'none';
      graphModeSelect = false;
      selectDataButtonLabel = "zoom mode";
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

    <Toggle on:change={() => selectDataClick()}>Select mode</Toggle>
    <div class="left-dropdown">

    <Badge color="green">{`Mode: ${selectDataButtonLabel}`}</Badge>
  
    </div>

    <div class="left-dropdown">
    <Button on:click={() => (formModal = true)}>Form modal</Button>
    </div>


{/if}
    <Modal bind:open={formModal} size="xs" autoclose={false} class="w-full">
      <form class="flex flex-col space-y-6" action="#">
        <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Label Data</h3>
        <Label class="space-y-2">
          Select an option
          <Select class="mt-2" items={faultLabel} bind:value={selected} />
        </Label>
        <Label class="space-y-2">
          <span>Notes</span>
          <Textarea {...textareaprops} />
        </Label>
        <Button type="submit" class="w-full1">Submit</Button>
      </form>
    </Modal>

</main>

<style>
.left-dropdown {
    text-align: left;
}
</style>