<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="18%" class="documentAsides">
        <el-row :gutter="20">
          <el-col :span="14">
            <div class="document_title">私人文档</div>
          </el-col>
          <el-col :span="10">
            <a class="action-button add2" @click="appendRoot">添加根目录</a>
          </el-col>
        </el-row>
        <div class="custom-tree-container">
          <el-input
            v-model="filterText"
            style="width: 100%; padding: 10px"
            placeholder="过滤关键字"
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
              <span class="custom-tree-node">
                <span v-if="node.label">{{ node.label }}</span>
                <span v-else>
                  <el-input
                    v-model="treeInputText"
                    ref="treeInput"
                    @blur="changeTree(node, data)"
                    style="width: 150px; height: 20px;"
                    placeholder="请输入"
                  />
                </span>
                <span>
                  <a class="action-button delete" @click="confirmDelete(node, data)">
                    <el-icon><Minus /></el-icon>
                  </a>
                  <a class="action-button add" @click="append(data)">
                    <el-icon><Plus /></el-icon>
                  </a>
                  <a class="action-button edit" @click="edit(node, data)">
                    <el-icon><Edit /></el-icon>
                  </a>
                </span>
              </span>
            </template>
          </el-tree>
        </div>
      </el-aside>

      <el-main >
        <el-row :gutter="20" class="el-button-group">
          <el-col :span="2"><el-button type="primary" @click="addRow">添加行</el-button></el-col>
          <el-col :span="2"><el-button type="primary" @click="addColumn">添加列</el-button></el-col>
          <el-col :span="2"><el-button type="primary" @click="addText">添加文本</el-button></el-col>
        </el-row>

        <div v-if="tableData.length > 0">
          <el-table border stripe :data="tableData"  style="width: 100%" max-height="600">
            <el-table-column
              v-for="(col, colIndex) in dynamicColumns"
              :key="colIndex"
              :prop="col.prop"
              :label="col.label"
              width="120"
            >
              <template #default="scope">
                <div v-if="isEditingCell(scope.$index, colIndex)">
                  <el-input
                    v-model="tableData[scope.$index][col.prop]"
                    @blur="saveCell(scope.$index, colIndex)"
                    inline
                  />
                </div>
                <div v-else @click="editCell(scope.$index, colIndex)">
                  {{ scope.row[col.prop] }}
                </div>
              </template>
              <template #header="scope">
                <span>{{ scope.column.label }}</span>
                <el-button
                  type="danger" :icon="Delete" circle size="small"
                  @click="deleteColumn(colIndex)"
                />
              </template>
            </el-table-column>
            <el-table-column fixed="right" label="操作" min-width="120">
              <template #default="scope">
                <el-button link type="primary" size="small" @click="deleteRow(scope.$index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table></div>
        <h3></h3>
        <div v-if="tableData.length > 0 && (datatext||textbuttoon)"  >
          <el-input placeholder="请输入内容" type="textarea" autosize v-model="datatext"></el-input>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script lang="ts" setup>
import { ref, nextTick, watch, onMounted, computed } from 'vue'
import { ElTree, ElMessageBox, ElMessage, ElIcon } from 'element-plus'
import axios from 'axios'
import {
  Check,
  Delete,
  Edit,
  Message,
  Search,
  Star,
} from '@element-plus/icons-vue'
interface Tree {
  id: number
  label: string
  children?: Tree[]
}

const datatext = ref('')
const dataSource = ref<Tree[]>([])
const treeInput = ref()
const treeInputText = ref('')
const filterText = ref('')
const treeRef = ref<InstanceType<typeof ElTree>>()
const tableData = ref([])
const dynamicColumns = ref([])
const selectedTreeId = ref<number | null>(null)
const editingCell = ref({ rowIndex: null, colIndex: null })
const textbuttoon = ref(false)


const generateId = () => 'cc' + Date.now()

const appendRoot = async () => {
  dataSource.value.push({ id: generateId(), label: '新根节点', children: [] })
  await nextTick()
}

const append = async (data: Tree) => {
  if (!data.children) data.children = []
  data.children.push({ id: generateId(), label: '新节点', children: [] })
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

const filterNode = (value, data) => {
  if (!value) return true
  return data.label.includes(value)
}

watch(filterText, (val) => {
  treeRef.value!.filter(val)
})

const fetchData = async (id: number) => {
  tableData.value = []
  dynamicColumns.value = []
  datatext.value = ''
  textbuttoon.value = false
  try {
    const response = await axios.get('http://10.2.3.117:8000/doc/GetData', {
      params: { treeid: id.toString() }
    })
    const data = response.data
    const column0Data = JSON.parse(data.column0.replace(/'/g, '"'))
    datatext.value = data.column1
    const columns = []
    const rows = []


    column0Data.forEach((col, index) => {
      const colName = Object.keys(col)[0]
      const colData = col[colName]
      columns.push({ prop: `col${index}`, label: colName })
      colData.forEach((value, rowIndex) => {
        if (!rows[rowIndex]) rows[rowIndex] = {}
        rows[rowIndex][`col${index}`] = value
      })
    })

    dynamicColumns.value = columns
    tableData.value = rows

    console.log(tableData)
  } catch (error) {
    console.error('获取数据时出错:', error)
  }
}

const fetchTreeData = async () => {
  try {
    const response = await axios.get('http://10.2.3.117:8000/doc/GetList', {
      params: { create_people: 'cc' }
    })
    dataSource.value = JSON.parse(response.data).tree_node
  } catch (error) {
    console.error('获取树数据时出错:', error)
  }
}

onMounted(() => {
  fetchTreeData()
})

const handleNodeClick = (data: Tree) => {
  selectedTreeId.value = data.id
  fetchData(data.id)
}


const addRow = () => {
  const newRow = {}
  dynamicColumns.value.forEach(col => newRow[col.prop] = '新值')
  tableData.value.push(newRow)
}

const addColumn = () => {
  const newColumnProp = `newColumn${dynamicColumns.value.length + 1}`
  dynamicColumns.value.push({ prop: newColumnProp, label: `新列 ${dynamicColumns.value.length + 1}` })
  tableData.value.forEach(row => row[newColumnProp] = '新值')
}

const addText = () => {
  textbuttoon.value = !textbuttoon.value  // 更新 tablebuttoon 的值
}

const deleteColumn = (colIndex) => {
  const columnProp = dynamicColumns.value[colIndex].prop
  dynamicColumns.value.splice(colIndex, 1)
  tableData.value.forEach(row => delete row[columnProp])
}

const confirmDelete = (node: Node, data: Tree) => {
  ElMessageBox.confirm(
    '你确定要删除此文档？？？',
    '删除',
    {
      confirmButtonText: '确认删除',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(() => {
      remove(node, data)
      ElMessage({ type: 'success', message: '删除完成' })
    })
    .catch(() => {
      ElMessage({ type: 'info', message: '已取消' })
    })
}

watch(dataSource, async (newValue) => {
  try {
    await axios.post('http://10.2.3.117:8000/doc/SaveList', {
      tree_list: newValue,
      create_people: 'cc',
      update_people: 'cc'
    })
  } catch (error) {
    console.error('保存数据时出错:', error)
  }
}, { deep: true })

watch([tableData, datatext, dynamicColumns], async () => {
  saveData()
}, { deep: true })

const saveData = async () => {
  if (selectedTreeId.value === null) {
    console.error('未选择树节点')
    return
  }

  const clsData = dynamicColumns.value.map(col => ({
    [col.label]: tableData.value.map(row => row[col.prop])
  }))

  const requestData = {
    cls: clsData.length > 0 ? clsData : [],
    datatext: datatext.value ? datatext.value.toString() : '',
    savepeople: 'cc',
    treeid: selectedTreeId.value.toString()
  }

  try {
    await axios.post('http://10.2.3.117:8000/doc/SubmitData', requestData)
  } catch (error) {
    console.error('保存数据时出错:', error)
  }
}

const deleteRow = (rowIndex) => {
  tableData.value.splice(rowIndex, 1)
}

const isEditingCell = (rowIndex, colIndex) => {
  return editingCell.value.rowIndex === rowIndex && editingCell.value.colIndex === colIndex
}

const editCell = (rowIndex, colIndex) => {
  editingCell.value = { rowIndex, colIndex }
}

const saveCell = (rowIndex, colIndex) => {
  editingCell.value = { rowIndex: null, colIndex: null }
}
</script>

<style scoped>
.common-layout {
  display: flex;
  flex-direction: row;
  height: 100vh;
  background-color: #f5f5f5;
}

.documentAsides {
  background-color: #fff;
  border-right: 1px solid #ebeef5;
  padding: 20px;
}

.document_title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.action-button {
  color: #409eff;
  cursor: pointer;
  margin-left: 10px;
}

.el-button-group{
  margin: 20px;
}

.action-button.add {
  color: #67c23a;
  float: right;
}

.action-button.add2 {
  color: #7bef49;
  float: right;
}

.action-button.delete {
  color: #f56c6c;
  float: right;
}

.action-button.edit {
  color: #6cd5f5;
  float: right;
}

.custom-tree-container {
  margin-top: 1px;
}

.custom-tree-node {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.custom-tree-node span {
  display: inline-block;
  margin-right: 10px;
}

.el-main {
  flex: 1;
  padding: 20px;
  background-color: #fff;
  overflow-y: auto;
}
</style>
