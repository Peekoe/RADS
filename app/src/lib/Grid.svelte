<script lang="ts">
  export let data: { string: {string: number} };
  const teams = Object.keys(data);

  const state = { "1": "win", "0": "tie", "-1": "lose" };
</script>

<table>
  <tr>
    <th>GRID</th>
    {#each teams as team}
      <th>{team.substring(0, 2)}</th>
    {/each}
  </tr>
  {#each Object.entries(data) as team}
    <tr>
      <td>{team[0].substring(0, 2)}</td>
      {#each Object.entries(team[1]) as result}
        <td class={state[result[1]]}></td>
      {/each}
    </tr>
  {/each}
</table>

<style>
  table {
    border-collapse: collapse;
    width: 100%;
    border-color: white;
  }

  th,
  td {
    text-align: center;
    border: 1px solid #bbc6ce;

    height: 2rem;
    width: 2rem;
  }

  .win {
    background-color: var(--correct);
    color: var(--background);
  }

  .lose {
    background-color: var(--wrong);
  }
</style>
