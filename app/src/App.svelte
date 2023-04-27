<script lang="ts">
  import radsLogo from "./assets/rads.png"

  const moves = ['RR', 'RA', 'RS', 'RD', 'AA', 'AS', 'AD', 'SS', 'SD', 'DD'];
  const normal_moves = moves.filter(w => !w.includes('R'));

  function submit() {
    console.log(form);
  }
</script>

<header>
  <img src={radsLogo} alt="RADS logo" id="logo">
  <h1>RADS</h1>
</header>

<main>
  <form on:submit|preventDefault={submit}>
    <label for="username">Username:</label>
    <input type="text" />
    
    <label for="public">My Public:</label>
    <input type="text" list="moves">
    
    <datalist id="moves">
      {#each moves as move}
        <option value={move}>{move}</option>
      {/each}
    </datalist>

    {#each normal_moves as move}
      <label for={move}>If {move}, play:</label>
      <input type="text" list="moves">
    {/each}

    <input type="submit" value="Submit Moves" />
  </form>
</main>

<footer>
  <sub>Frontend by Charlie<br>Game invented by Aaron & Christos</sub>
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
