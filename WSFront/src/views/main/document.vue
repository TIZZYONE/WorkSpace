<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="22%" class="documentAsides">
        <el-row :gutter="20">
          <el-col :span="14"><div class="document_title"> 私人文档</div></el-col>
          <el-col :span="8"><a class="action-button add" @click="appendRoot">添加根目录</a></el-col>
        </el-row>
        <div class="custom-tree-container">
          <el-input
            v-model="filterText"
            style="width: 100%;padding: 10px"
            placeholder="Filter keyword"
          />
          <el-tree
            ref="treeRef"
            style="max-width: 100%"
            :data="dataSource"
            draggable
            node-key="id"
            default-expand-all
            :filter-node-method="filterNode"
            :expand-on-click-node="false"
            @node-click="handleNodeClick"
          >
            <template #default="{ node, data }">
              <span class="custom-tree-node" >
                <span v-if="node.label">{{ node.label }}</span>
                <span v-else>
                  <el-input
                    v-model="treeInputText"
                    ref="treeInput"
                    @blur="changeTree(node, data)"
                    style="width: 150px; height: 20px;"
                    placeholder="Please input"
                  />
                </span>
                <span>
                  <a class="action-button edit" @click="edit(node, data)">编辑</a>
                  <a class="action-button add" @click="append(data)">添加</a>
                  <a class="action-button delete" @click="remove(node, data)">删除</a>
                </span>
              </span>
            </template>
          </el-tree>
        </div>
      </el-aside>
      <el-main>
        <el-button type="primary" @click="addRow">Add Row</el-button>
        <el-button type="primary" @click="addColumn">Add Column</el-button>
        <el-table border stripe :data="tableData" style="width: 100%" max-height="600">
          <el-table-column v-for="(col, index) in dynamicColumns" :key="index" :prop="col.prop" :label="col.label"
                           width="120" />
          <el-table-column fixed="right" label="Operations" min-width="120">
            <template #default>
              <el-button link type="primary" size="small" @click="handleClick">
                Detail
              </el-button>
              <el-button link type="primary" size="small">Edit</el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="data-source-display">
          <h3>Data Source</h3>
          <pre>{{ dataSourceString }}</pre>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script lang="ts" setup>
import { ref, nextTick, watch, onMounted, computed } from 'vue'
import type Node from 'element-plus/es/components/tree/src/model/node'
import { ElTree } from 'element-plus'
import axios from 'axios'

interface Tree {
  id: number
  label: string
  children?: Tree[]
}

const dataSource = ref<Tree[]>([])
let id = 100

const appendRoot = async () => {
  const newRoot = { id: id++, label: '新根节点', children: [] }
  dataSource.value.push(newRoot)
  await nextTick()
}

const append = async (data: Tree) => {
  const newChild = { id: id++, label: '新节点', children: [] }
  if (!data.children) {
    data.children = []
  }
  data.children.push(newChild)
  dataSource.value = [...dataSource.value]
  await nextTick()
}

const remove = (node: Node, data: Tree) => {
  const parent = node.parent
  const children: Tree[] = parent.data.children || parent.data
  const index = children.findIndex((d) => d.id === data.id)
  children.splice(index, 1)
  dataSource.value = [...dataSource.value]
}

const edit = async (node: Node, data: Tree) => {
  treeInputText.value = data.label
  data.label = ''
  await nextTick()
  treeInput.value.focus()
}

const changeTree = (node: Node, data: Tree) => {
  data.label = treeInputText.value
}

const treeInput = ref()
const treeInputText = ref('')

const filterText = ref('')
const treeRef = ref<InstanceType<typeof ElTree>>()

watch(filterText, (val) => {
  treeRef.value!.filter(val)
})

const filterNode = (value: string, data: Tree) => {
  if (!value) return true
  return data.label.includes(value)
}

const tableData = ref([])
const dynamicColumns = ref([])

const fetchData = async (id: number) => {
  try {
    const response = await axios.get('http://10.2.3.117:8000/doc/GetData', {
      params: { name: id } // 使用当前 tree 的 id
    })
    const data = response.data
    console.log(data)

    // 动态生成列
    dynamicColumns.value = Object.keys(data).map((key, index) => ({
      prop: key,
      label: data[key].split('=')[0] // 使用等号前的部分作为列名
    }))

    // 获取最大行数
    const maxRows = Math.max(...Object.values(data).map(val => val.match(/\[(.*?)\]/)[1].split(',').length))

    // 初始化表格数据
    tableData.value = Array.from({ length: maxRows }, () => ({}))

    // 填充表格数据
    Object.keys(data).forEach((key, colIndex) => {
      const values = data[key].match(/\[(.*?)\]/)[1].split(',')
      values.forEach((value, rowIndex) => {
        tableData.value[rowIndex][key] = value.trim().replace(/['"]+/g, '')
      })
    })
  } catch (error) {
    console.error('Error fetching data:', error)
  }
}

const fetchTreeData = async () => {
  try {
    const response = await axios.get('http://10.2.3.117:8000/doc/GetList', {
      params: { create_people: 'cc' } // 这里替换为你需要查询的创建人
    })
    const data = response.data
    console.log(data)

    // 将返回的数据赋值给 dataSource
    dataSource.value = JSON.parse(data).tree_node
  } catch (error) {
    console.error('Error fetching tree data:', error)
  }
}

// 在组件挂载时获取数据
onMounted(() => {
  fetchTreeData()
})

// 处理节点点击事件
const handleNodeClick = (data: Tree) => {
  fetchData(data.id)
}

const handleClick = () => {
  console.log('click')
}

const addRow = () => {
  const newRow = {}
  dynamicColumns.value.forEach(col => {
    newRow[col.prop] = 'New Value'
  })
  tableData.value.push(newRow)
}

const addColumn = () => {
  const newColumnProp = `newColumn${dynamicColumns.value.length + 1}`
  dynamicColumns.value.push({
    prop: newColumnProp,
    label: `New Column ${dynamicColumns.value.length + 1}`
  })
  // Add the new property to each existing row
  tableData.value.forEach(row => {
    row[newColumnProp] = 'New Value'
  })
}

// 计算属性：将 dataSource 转换为字符串
const dataSourceString = computed(() => {
  return JSON.stringify(dataSource.value, null, 2)
})

// 监听 dataSource 的变化并发送请求
watch(dataSource, async (newValue) => {
  try {
    const response = await axios.post('http://10.2.3.117:8000/doc/SaveList', {
      tree_list: newValue,
      create_people: 'cc',
      update_people: 'cc'
    })
    console.log('Data saved successfully:', response.data)
  } catch (error) {
    console.error('Error saving data:', error)
  }
}, { deep: true })
</script>

<style scoped>
.document_title{
  font-size: 20px;
  font-weight: bold;
  color: #000000;
  margin: 10px 0;
  padding-left: 20px;
  text-align: left;
  font-family: Arial, sans-serif;
}

.documentAsides{
  height: 100vh;
  margin-right: 50px;
}
.common-layout{
  background-color: #ffffff;
}
.custom-tree-node.first-level {
  font-size: 20px;
  font-weight: bold;
  color: #000000;
  margin: 10px 0;
  text-align: left;
  font-family: Arial, sans-serif;
}
</style>
