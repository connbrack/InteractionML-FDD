<script>
import {
    page
} from '$app/stores';
import {
    Navbar,
    NavBrand,
    NavLi,
    NavUl,
    NavHamburger
} from 'flowbite-svelte';

$: activeUrl = $page.url.pathname;
</script>

<main>
    <Navbar let:hidden let:toggle>
        <NavBrand href="/">
            <img src="/src/images/logo.png" class="mr-3 h-6 sm:h-9" alt="logo" />
            <span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">Interaction FDD</span>
        </NavBrand>
        <NavHamburger on:click={toggle} />
        <NavUl {activeUrl} {hidden}>
            <NavLi href="/">Home</NavLi>
            <NavLi href="/dataView">View Data</NavLi>
            <NavLi href="/dataSelect">Select Data</NavLi>
            <NavLi href="/timeSim">Time Adjuster</NavLi>
        </NavUl>
    </Navbar>
</main>
<hr style="width:100%;text-align:left;margin-left:0">

<style>
main {
    padding: 2px;
}
</style>
