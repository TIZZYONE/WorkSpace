<script lang="ts" setup>
import { ref } from 'vue'
import { Menu as IconMenu, Message, Setting } from '@element-plus/icons-vue'
const activeIndex = ref('1')
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>


<template>
    <el-container class="el-container">
      <el-aside width="200px" class="asides">
        <!--        下面这个是侧边栏滚动条 scrollbar 删掉就没有-->
        <el-scrollbar>

          <el-menu :router=true :default-openeds="['1', '3']"  class=".asides .el-menu">
            <router-link to="/index" class="title">TIZZY</router-link>
            <el-sub-menu index="1">
              <template #title>
                <el-icon>
                  <message />
                </el-icon>
                小功能
              </template>
              <el-menu-item-group>
                <template #title>Group 1</template>
                <el-menu-item index="1-1" :route="{name:'document'}">随笔</el-menu-item>
                <el-menu-item index="1-1" :route="{name:'eat'}">今天吃啥</el-menu-item>
                <el-menu-item index="1-2" :route="{name:'cs'}">Option 2</el-menu-item>
              </el-menu-item-group>
              <el-menu-item-group title="Group 2">
                <el-menu-item index="1-3" :route="{name:'csone'}">csone</el-menu-item>
              </el-menu-item-group>
              <el-sub-menu index="1-4">
                <template #title>Option4</template>
                <el-menu-item index="1-4-1">Option 4-1</el-menu-item>
              </el-sub-menu>
            </el-sub-menu>
          </el-menu>
        </el-scrollbar>
      </el-aside>
      <el-container>
        <el-header class="headers">
          <el-menu
            :default-active="activeIndex"
            class="el-menu-demo"
            mode="horizontal"
            @select="handleSelect"
          >
            <el-menu-item index="1">Processing Center</el-menu-item>
            <el-sub-menu index="2">
              <template #title>Workspace</template>
              <el-menu-item index="2-1">item one</el-menu-item>
              <el-menu-item index="2-2">item two</el-menu-item>
              <el-menu-item index="2-3">item three</el-menu-item>
              <el-sub-menu index="2-4">
                <template #title>item four</template>
                <el-menu-item index="2-4-1">item one</el-menu-item>
                <el-menu-item index="2-4-2">item two</el-menu-item>
                <el-menu-item index="2-4-3">item three</el-menu-item>
              </el-sub-menu>
            </el-sub-menu>
            <el-menu-item index="3" disabled>Info</el-menu-item>
            <el-menu-item index="4">Orders</el-menu-item>
          </el-menu>
        </el-header>
          <el-main class="mains">
            <router-view></router-view>
          </el-main>
<!--          <el-footer>Footer</el-footer>-->
      </el-container>
    </el-container>
</template>
<style scoped>

.el-container {
  padding: 0px;
  margin: 0px;
  height: 100vh;
  width: 100%;
}
.asides {
  margin:0px;
  padding: 0px;
  height: 100vh;
}
.asides .el-menu {
  margin: 0px;
  height: 100vh;
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}

.title {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #7b7bea;
  font-size: 28px;
  text-decoration: none;
}
.mains{
  padding: 18px;
  background-color: #ebeef5;
}

.headers{
  margin:0px;
  padding: 0px;
  width: 100%;
  height: 60px;
}


</style>
