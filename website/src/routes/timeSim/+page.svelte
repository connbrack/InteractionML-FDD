<script>
import moment from "moment";
import RangeSlider from "svelte-range-slider-pips";
import {
    onMount
} from 'svelte'
import {
    Button,
    Dropdown,
    DropdownItem,
} from 'flowbite-svelte';
import {
    Icon
} from 'flowbite-svelte-icons';
import {
    serverIP
} from '$lib/localstore.js';

// Slider
let sliderValues = [1, 365];
let faultValues = [1, 365];

const formatter = (value) => moment('2019-01-01').add(value - 1, 'days').format('MMM-DD');
function mainSliderChange() {
    let min = sliderValues[0];
    let max = sliderValues[1];
    if (Math.max(...faultValues) > max) {
        faultValues = [faultValues[0], max];
    }
    if (Math.min(...faultValues) < min) {
        faultValues = [min, faultValues[1]];
    }
}

function faultSliderChange() {
    let min = faultValues[0];
    let max = faultValues[1];
    if (Math.max(...sliderValues) < max) {
        sliderValues = [sliderValues[0], max];
    }
    if (Math.min(...faultValues) > min) {
        sliderValues = [min, sliderValues[1]];
    }
}

// Buttons

let isOpen = false;
let fault = 'coi_leakage_025_annual'
let faultList = [];
let faultCount = 0;

const dropdownClick = async (selectedFault) => {
    fault = selectedFault;
    closeDropdown();
}

const closeDropdown = () => {
    isOpen = false;
};
const addFault = async () => {
    if (faultCount < 1) {
        faultCount++;
    };
}
const removeFault = async () => {
    if (faultCount > 0) {
        faultCount--;
    }
}

// API functions
const getAHUsensors = async () => {
    const response = await fetch(`${serverIP}/AHU_fault_list`)
    const data = await response.json();
    faultList = data;
}
onMount(async () => {
    getAHUsensors();
});
</script>

<main>

    <h2 class="left">Primary data set</h2>
    <RangeSlider
        on:change={() => { mainSliderChange() }}
        range pips float
        min={1} max={365}
        {formatter}
        springValues={{ stiffness: 0.32, damping: 1 }}
        bind:values={sliderValues} />
    ({formatter(sliderValues[0])} - {formatter(sliderValues[1])})

    <br /> <br /> <br />

    {#if faultCount >= 1}
    <div class="left">
        Fault:
        <Button outline size='sm'>{fault}<Icon name="chevron-down-solid" class="w-2 h-3 ml-2 text-purple dark:text-white" /></Button>
        <Dropdown bind:open={isOpen} class="overflow-y-auto py-1 h-64 whitespace-nowrap left-0" placement="bottom">
            {#each Object.entries(faultList) as [key, fault]}
            <DropdownItem on:click={() => dropdownClick(fault['Faults'])}>{fault['Faults']}</DropdownItem>
            {/each}
        </Dropdown>
    </div>

    <RangeSlider
        on:change={() => { faultSliderChange() }}
        range pips float 
        min={1} max={365}
        {formatter}
        springValues={{ stiffness: 0.32, damping: 1 }}
        bind:values={faultValues} />
    ({formatter(faultValues[0])} - {formatter(faultValues[1])})
    <br /> <br /> <br />
    {/if}

    <div class='left'>
        <Button on:click={() => addFault()}>Add fault</Button>
        <Button on:click={() => removeFault()}>Remove fault</Button>
    </div>
    <Button>Apply</Button>
</main>

<style>
:root {
    --range-slider: #d7dada;
    --range-handle-inactive: #7E22CE;
    --range-handle: #7E22CE;
    --range-handle-focus: #7E22CE;
    --range-handle-border: var(--range-handle);
    --range-range-inactive: var(--range-handle-inactive);
    --range-range: var(--range-handle-focus);
    --range-float-inactive: var(--range-handle-inactive);
    --range-float: var(--range-handle-focus);
    --range-float-text: white;
}

.left {
    text-align: left;
}
</style>
