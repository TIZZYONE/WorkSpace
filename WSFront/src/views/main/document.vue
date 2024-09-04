<script lang="ts" setup>
import { ref } from 'vue'

const handleClick = () => {
  console.log('click')
}

const tableData = ref([
  {
    date: '2016-05-03',
    name: '1',
    state: '2',
    city: '首页的main后期做报表',
    address: 'doc后端实现提供数据',
    zip: 'doc前端展示数据',
    tag: '添加列  添加行',
  },
  {
    date: '2016-05-02',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
    tag: 'Office',
  },
  {
    date: '2016-05-04',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
    tag: 'Home',
  },
  {
    date: '2016-05-01',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
    tag: 'Office',
  },
])

const dynamicColumns = ref([])

const addRow = () => {
  tableData.value.push({
    date: '2023-10-01',
    name: 'New Name',
    state: 'New State',
    city: 'New City',
    address: 'New Address',
    zip: 'New Zip',
  })
}

const addColumn = () => {
  const newColumnProp = `newColumn${dynamicColumns.value.length + 1}`
  dynamicColumns.value.push({
    prop: newColumnProp,
    label: `New Column ${dynamicColumns.value.length + 1}`,
  })
  // Add the new property to each existing row
  tableData.value.forEach(row => {
    row[newColumnProp] = 'New Value'
  })
}
</script>

<template>
  <div>
    <el-button type="primary" @click="addRow">Add Row</el-button>
    <el-button type="primary" @click="addColumn">Add Column</el-button>
    <el-table border stripe :data="tableData" style="width: 100%" max-height="600">
      <el-table-column fixed prop="date" label="Date" width="150" />
      <el-table-column prop="name" label="Name" width="120" />
      <el-table-column prop="state" label="State" width="120" />
      <el-table-column prop="city" label="City" width="120" />
      <el-table-column prop="address" label="Address" width="600" />
      <el-table-column prop="zip" label="Zip" width="120" />
      <el-table-column v-for="(col, index) in dynamicColumns" :key="index" :prop="col.prop" :label="col.label" width="120" />
      <el-table-column fixed="right" label="Operations" min-width="120">
        <template #default>
          <el-button link type="primary" size="small" @click="handleClick">
            Detail
          </el-button>
          <el-button link type="primary" size="small">Edit</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<style scoped>

</style>