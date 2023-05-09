<script lang="ts">
  import { onMount } from "svelte";
  import { io, Socket } from "socket.io-client";
  import radsLogo from "./assets/rads.png";
  import Leaderboard from "./lib/Leaderboard.svelte";
  import Grid from "./lib/Grid.svelte";

  const moves = ["RR", "RA", "RS", "RD", "AA", "AS", "AD", "SS", "DS", "DD"];

  const normal_moves = moves.filter((w) => !w.includes("R"));
  let name = "";
  let board: boolean = false;
  let ws: Socket;
  let error: boolean = false;

  let data = {
    peekoe: { peekoe: 0, christos: -1, yao: 0 },
    christos: { peekoe: 1, christos: 0, yao: 0 },
    yao: { christos: 0, peekoe: 0, yao: 0 },
  };

  function onSubmit(e) {
    const formData = new FormData(e.target);
    name = formData.get("username").valueOf().toString();

    let json = Object.fromEntries(formData.entries());
    console.log(json);

    ws.emit("json", JSON.stringify(json));
  }

  onMount(() => {
    console.log("here");
    ws = io("ws://137.151.29.178:80");
    error = ws === undefined;
    console.log(error);

    ws.on("NEXT", () => {
      board = false;
    });

    ws.on("json", (event) => {
      data = event;
      board = true;
    });
  });
</script>

<header>
  <img src={radsLogo} alt="RADS logo" id="logo" />
  <h1>RADS</h1>

  {#if error}
    <div class="error">Could not connect to game server!</div>
  {/if}
</header>

<main>
  {#if board}
    <div class="all_results">
      <div class="results">
        <div class="board">
          <Leaderboard name={name} teams={data[name]} />
        </div>
        <div class="grid">
          <Grid {data} />
        </div>
      </div>
      <hr />
      <div class="contain_other_boards">
        {#each Object.entries(data).filter((t) => t[0] !== name) as team}
          <div class="other_boards">
            <Leaderboard name={team[0]} teams={team[1]} />
          </div>
        {/each}
      </div>
    </div>
  {:else}
    <form on:submit|preventDefault={onSubmit}>
      <div class="grid">
        <label for="username">
          Username:
          <input type="text" id="username" name="username" />
        </label>

        <label for="public">
          My Public:
          <input type="text" id="public" name="public" />
        </label>
      </div>

      <datalist id="moves" />

      {#each normal_moves as move}
        <label for={move}>
          If {move} play:
          <select name={move} id={move}>
            {#each moves as move}
              <option value={move}>{move}</option>
            {/each}
          </select>
        </label>

        <!-- <label for={move}>
          If {move}, play:
          <input type="text" id={move} name={move} />
        </label> -->
      {/each}

      <input type="submit" value="Submit Moves" />
    </form>
  {/if}
</main>

<footer>
  <small>Frontend by Charlie<br />Game invented by Aaron & "christos"</small>
</footer>

<style>
  header {
    display: flex;
    flex-direction: row;
    /* position: absolute;
    top: 0;
    height: 3rem; */
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
    height: 100%;
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

  .all_results {
    display: flex;
    flex-direction: column;
    height: 100%;
    justify-content: center;
  }

  .results {
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
    align-items: center;
  }

  .board {
    display: flex;
    justify-content: space-evenly;
    margin: 1rem;
    width: 30vw;
  }

  .contain_other_boards {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: space-between;
  }

  .other_boards {
    width: 45%;
    margin: 1rem;
  }

  .grid {
    width: auto;
    height: auto;
    margin: 1rem;
  }

  footer {
    bottom: 0;
    height: 4rem;
    margin: 1rem;
  }

  @media screen and (max-width: 480px) {
    form {
      width: 80vw;
    }

    .results {
      flex-direction: column-reverse;
      width: 100%;
    }

    .board {
      width: 70%;
    }

    .contain_other_boards {
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 70vw;
    }

    .other_boards {
      width: 70%;
    }
  }
</style>
