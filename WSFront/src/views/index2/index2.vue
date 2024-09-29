<script lang="ts" setup>
import { ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'

import type { UploadProps, UploadUserFile } from 'element-plus'

const activeIndex = ref('1')
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
const fileList = ref<UploadUserFile[]>([
  {
    name: 'food.jpg',
    url: 'static\\img\\ccwwimg\\20240926194504.jpg'
  },
  {
    name: 'food-1.jpg',
    url: 'static\\img\\ccwwimg\\微信图片_20240926194507.jpg'
  },
  {
    name: 'food-2.jpg',
    url: 'static\\img\\ccwwimg\\微信图片_20240926194512.jpg'
  },
  {
    name: 'food-3.jpg',
    url: 'static\\img\\ccwwimg\\微信图片_20240926194514.jpg'
  },
  {
    name: 'food-4.jpg',
    url: 'static\\img\\ccwwimg\\微信图片_20240926194515.jpg'
  },
  {
    name: 'food-5.jpg',
    url: 'static\\img\\ccwwimg\\微信图片_20240926194518.jpg'
  },
  {
    name: 'food-6.jpg',
    url: 'static\\img\\ccwwimg\\微信图片_20240926194519.jpg'
  },
  {
    name: 'food-7.jpg',
    url: 'static\\img\\ccwwimg\\微信图片_20240926194520.jpg'
  },
  {
    name: 'food-8.jpg',
    url: 'static\\img\\ccwwimg\\微信图片_20240926194521.jpg'
  },
  {
    name: 'food-9.jpg',
    url: 'static\\img\\ccwwimg\\微信图片_20240926194523.jpg'
  },
  {
    name: 'food-10.jpg',
    url: 'static\\img\\ccwwimg\\微信图片_20240926194525.jpg'
  },
  {
    name: 'food-11.jpg',
    url: 'static\\img\\ccwwimg\\微信图片_20240926194526.jpg'
  },

  {
    name: 'food-13.jpg',
    url: 'static\\img\\ccwwimg\\微信图片_202409261945141.jpg'
  },
  {
    name: 'food-14.jpg',
    url: 'static\\img\\ccwwimg\\微信图片_202409261945231.jpg'
  },
  {
    name: 'food-15.jpg',
    url: 'static\\img\\ccwwimg\\微信图片_202409261945251.jpg'
  },
])

const dialogImageUrl = ref('')
const dialogVisible = ref(false)

const handleRemove: UploadProps['onRemove'] = (uploadFile, uploadFiles) => {
  console.log(uploadFile, uploadFiles)
}

const handlePictureCardPreview: UploadProps['onPreview'] = (uploadFile) => {
  dialogImageUrl.value = uploadFile.url!
  dialogVisible.value = true
}

const zmdimages = ref([
  'static\\img\\zmd1.jpg',
  'static\\img\\zmd2.jpg',
  'static\\img\\zmd3.jpg',
  'static\\img\\zmd4.jpg'
])

</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          :ellipsis="false"
          @select="handleSelect"
        >
          <el-menu-item index="0">
            <img
              style="width: 90px"
              src="C:\C\PycharmProjects_ALLIN\WorkSpace\WSFront\static\img\labubu.jpg"
              alt="Element logo"
            />
          </el-menu-item>
          <el-sub-menu index="2">
            <template #title>CC&WW</template>
            <el-menu-item index="2-1">2024.10.2</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-header>
      <el-container>
        <el-aside width="20%"></el-aside>
        <el-main>
          <h1></h1>
          <div class="block text-center">
            <el-carousel :interval="4000" arrow="always">
              <el-carousel-item v-for="(item, index) in zmdimages" :key="index">
                <img :src="item" class="carousel-image" />
              </el-carousel-item>
            </el-carousel>
          </div>

          <el-upload
            v-model:file-list="fileList"
            action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
            list-type="picture-card"
            :on-preview="handlePictureCardPreview"
            :on-remove="handleRemove"
          >
            <el-icon>
              <Plus />
            </el-icon>
          </el-upload>

          <el-dialog v-model="dialogVisible">
            <img class="w-full" :src="dialogImageUrl" alt="Preview Image" />
          </el-dialog>

        </el-main>
        <el-aside width="20%"></el-aside>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped>
.el-menu--horizontal > .el-menu-item:nth-child(1) {
  margin-right: auto;
}

.demonstration {
  color: var(--el-text-color-secondary);
}

.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
.el-menu-demo{
  height: 100px;
}
.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 使图片覆盖整个容器，同时保持其比例 */
}
</style>
