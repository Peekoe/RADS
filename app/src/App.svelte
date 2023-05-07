<script lang="ts">
  import { onMount } from "svelte";
  import radsLogo from "./assets/rads.png";
  import Leaderboard from "./lib/Leaderboard.svelte";
  import Grid from './lib/Grid.svelte';

  const moves = ["RR", "RA", "RS", "RD", "AA", "AS", "AD", "SS", "SD", "DD"];
  const normal_moves = moves.filter((w) => !w.includes("R"));
  let name = "peekoe";
  let board: boolean = true;
  let ws: WebSocket;
  let error: boolean = false;

  let data = {
    peekoe: { peekoe: 0, christos: -1, yao: 0 },
    christos: { peekoe: 1, christos: 0, yao: 0 },
    yao: { christos: 0, peekoe: 0, yao: 0 },
  };

  async function onSubmit(e) {
    const formData = new FormData(e.target);
    name = formData["username"];
    let json = Object.fromEntries(formData.entries());

    ws.send(JSON.stringify(json));
  }

  onMount(() => {
    ws = new WebSocket("ws://137.151.29.178:80");
    error = ws === undefined;

    ws.addEventListener("message", (event) => {
      board = event.data !== "NEXT";
      if (board) data = JSON.parse(event.data);
    });
  });
</script>

<header>
  <img src={radsLogo} alt="RADS logo" id="logo" />
  <h1>RADS</h1>

  {#if error}
    <div class="error">
      Could not connect to game server!
    </div>
  {/if}
</header>

<main>
  {#if board}
    <div class="board">
      <Leaderboard name={name} teams={data[name]} />
      <Grid data={data} />
    </div>
  {:else}
    <form on:submit|preventDefault={onSubmit}>
      <label for="username">Username:</label>
      <input type="text" id="username" name="username" />

      <label for="public">My Public:</label>
      <input type="text" id="public" name="public" />

      <datalist id="moves">
        {#each moves as move}
          <option value={move}>{move}</option>
        {/each}
      </datalist>

      {#each normal_moves as move}
        <label for={move}>If {move}, play:</label>
        <input type="text" id={move} name={move} />
      {/each}

      <input type="submit" value="Submit Moves" />
    </form>
  {/if}
</main>

<footer>
  <sub>Frontend by Charlie<br />Game invented by Aaron & Christos</sub>
</footer>

<style>
  header {
    display: flex;
    flex-direction: row;
    margin: 1rem;
  }

  #logo {
    height: 2rem;
    width: 2rem;
    margin: 0.5rem;
  }

  main {
    display: flex;
    justify-content: center;
  }

  form {
    width: 30vw;
    display: flex;
    justify-content: center;
    flex-direction: column;
  }

  .error {
    height: 10%;
    margin-left: auto;
    border-radius: 0.25rem;
    padding: 0.5rem;
    background-color: darkred;
    color: white;
  }

  .board {
    margin: 1rem;
    width: 30vw;
  }

  footer {
    margin: 0.5rem;
  }

  @media screen and (max-width: 480px) {
    form {
      width: 80vw;
    }
  }
</style>
