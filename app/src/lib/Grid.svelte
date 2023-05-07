<script lang="ts">
  export let data: { string: {string: number} };
  console.log(data);
  const teams = Object.keys(data);

  const state = { "1": "win", "0": "tie", "-1": "lose" };
</script>

<table>
  <tr>
    <th>GRID</th>
    {#each teams as team}
      <th>{team}</th>
    {/each}
  </tr>
  {#each Object.entries(data) as team}
    <tr>
      <td>{team[0]}</td>
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
    padding: 10px;
    border: 1px solid #bbc6ce;
  }

  th {
  }

  .win {
    background-color: #04E762;
    color: #11191f;
  }

  .lose {
    background-color: #960200;
  }
</style>
