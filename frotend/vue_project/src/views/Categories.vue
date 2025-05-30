<template>
  <div class="categories-view">
    <div class="flex justify-between items-center mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 mb-1">图书分类</h1>
        <p class="text-gray-600">共 {{ bookStore.categories.length }} 个分类</p>
      </div>
    </div>
    
    <!-- 分类卡片网格 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" v-loading="bookStore.loading">
      <el-card 
        v-for="category in bookStore.categories" 
        :key="category.id"
        class="category-card hover:shadow-md transition-shadow duration-300"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <el-icon class="text-primary text-2xl mr-3"><Folder /></el-icon>
            <div>
              <h3 class="text-xl font-medium">{{ category.name }}</h3>
              <p class="text-gray-500">{{ category.count || 0 }} 本图书</p>
            </div>
          </div>
          
          <div>
            <el-button size="small" @click="viewCategory(category)">查看图书</el-button>
          </div>
        </div>
      </el-card>
    </div>
    
    <!-- 分类统计图表 -->
    <div class="mt-10 bg-white p-6 rounded-lg shadow-sm">
      <h2 class="text-xl font-bold mb-4">分类统计</h2>
      <div ref="chartRef" style="width: 100%; height: 400px;"></div>
    </div>
    
    <!-- 分类详情对话框 -->
    <el-dialog
      v-model="showCategoryDialog"
      :title="selectedCategory ? selectedCategory.name : '分类详情'"
      width="900px"
      destroy-on-close
      v-if="selectedCategory"
      @close="handleDialogClose"
      :before-close="handleBeforeClose"
    >
      <div v-loading="categoryBooksLoading">
        <div class="mb-4">
          <h3 class="text-lg font-medium mb-2">分类信息</h3>
          <p v-if="selectedCategory.description">{{ selectedCategory.description }}</p>
          <p v-else class="text-gray-500">暂无描述</p>
        </div>
        
        <div class="mb-4">
          <h3 class="text-lg font-medium mb-2">包含图书 ({{ categoryBooks.length }})</h3>
          
          <div v-if="categoryBooks.length === 0" class="text-center text-gray-500 py-6">
            该分类下暂无图书
          </div>
          
          <el-table v-else :data="categoryBooks" style="width: 100%" border stripe v-loading="categoryBooksLoading">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column label="封面" width="100">
          <template #default="{ row }">
            <div class="flex items-center justify-center">
              <el-image
                style="width: 70px; height: 100px"
                :src="getBookCoverUrl(row.id, row.title)"
                :preview-src-list="[getBookCoverUrl(row.id, row.title)]"
                fit="cover"
                lazy
                :z-index="10"
              >
                <template #error>
                  <div class="flex items-center justify-center h-full w-full bg-gray-100">
                    <el-icon class="text-gray-400"><Picture /></el-icon>
                  </div>
                </template>
              </el-image>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="书名" min-width="180" />
        <el-table-column prop="author" label="作者" min-width="120" />
        <el-table-column prop="publisher" label="出版社" min-width="150" />
        <el-table-column prop="price" label="价格" width="100">
          <template #default="{ row }">
            <span class="font-medium" v-if="row.price !== undefined && row.price !== null">
              ¥{{ typeof row.price === 'number' ? row.price.toFixed(2) : parseFloat(row.price).toFixed(2) }}
            </span>
            <span class="text-gray-500" v-else>暂无价格</span>
          </template>
        </el-table-column>
            <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
                <el-button size="small" @click="viewBook(row)">查看</el-button>
          </template>
        </el-table-column>
      </el-table>
        </div>
        </div>
      
      <template #footer>
        <div class="flex justify-end">
          <el-button @click="showCategoryDialog = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick, onUnmounted, onBeforeUnmount, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useBookStore } from '../stores/bookStore'
import { ElMessage } from 'element-plus'
import { Folder, Picture } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { categoryApi, clearApiCache } from '../services/api'
import { mediaUtils } from '../services/api'

const router = useRouter()
const route = useRoute()
const bookStore = useBookStore()

// 状态变量
const chartRef = ref(null)
const chart = ref(null)
const showCategoryDialog = ref(false)
const selectedCategory = ref(null)
const categoryBooks = ref([])
const categoryBooksLoading = ref(false)
const isFirstLoad = ref(true) // 标记是否是首次加载

// 添加路由监听，每当路由到分类页面时刷新数据
watch(() => route.path, async (newPath, oldPath) => {
  // 当路由到达分类页面时
  if (newPath === '/categories' && oldPath !== '/categories') {
    console.log('从其他页面进入分类页面，准备重新获取数据')
    
    // 清除API缓存
    clearApiCache()
    
    // 重新获取数据
    try {
      bookStore.loading = true
      
      // 获取最新的分类数据
      console.log('正在重新获取分类数据...')
      await bookStore.fetchCategories()
      
      // 重新获取图书数据并更新分类图书数量
      console.log('正在重新获取图书数据和更新分类数量...')
      await bookStore.fetchBooks()
      await bookStore.updateCategoriesBookCount()
      
      // 更新图表
      nextTick(() => {
        if (chart.value) {
          updateChartData()
        } else {
          initChart()
        }
      })
    } catch (error) {
      console.error('路由进入分类页面后刷新数据失败:', error)
      ElMessage.error('更新分类数据失败，请尝试刷新页面')
    } finally {
      bookStore.loading = false
    }
  }
}, { immediate: true })

// 路由参数处理函数
const handleRouteParams = () => {
  // 检查URL中是否有category_id参数
  const urlCategoryId = route.query.category_id ? parseInt(route.query.category_id) : null;
  
  if (urlCategoryId && bookStore.categories.length > 0) {
    console.log(`尝试查找并打开分类ID: ${urlCategoryId}`);
    const category = bookStore.categories.find(c => c.id === urlCategoryId);
    
    if (category) {
      console.log(`找到分类: ${category.name}，准备打开详情`);
      // 清除URL参数，防止刷新页面时重复打开
      router.replace({ path: '/categories', query: {} });
      
      // 使用nextTick确保DOM更新后再打开对话框
      nextTick(() => {
        viewCategory(category);
      });
    } else {
      console.warn(`未找到ID为${urlCategoryId}的分类`);
    }
  }
};

// 监听路由变化
onMounted(() => {
  // 手动添加路由监听
  const routeListener = () => {
    // 只有当前在categories页面才处理
    if (route.path === '/categories') {
      console.log('检测到路由变化，当前在分类页面');
      // 立即关闭已打开的对话框
      showCategoryDialog.value = false;
      selectedCategory.value = null;
    }
  };
  
  // 添加监听
  window.addEventListener('popstate', routeListener);
  
  // 组件卸载时移除监听
  onBeforeUnmount(() => {
    window.removeEventListener('popstate', routeListener);
  });
});

// 初始化
onMounted(async () => {
  try {
    // 重置对话框状态，确保从其他页面切换回来时不会显示
    showCategoryDialog.value = false;
    selectedCategory.value = null;
    categoryBooks.value = [];
    
    // 只有在第一次加载时执行初始化，否则交给 watch 处理
    if (isFirstLoad.value) {
      isFirstLoad.value = false;
      
      // 加载状态
      bookStore.loading = true;
      
      // 清除API缓存
      clearApiCache();
      
      // 始终重新获取分类数据，确保每次都是最新的
      console.log('开始获取分类数据(首次加载)...');
      await bookStore.fetchCategories();
      
      // 获取图书数据
      console.log('开始获取图书数据(首次加载)...');
      await bookStore.fetchBooks();
      
      // 更新分类图书数量
      await bookStore.updateCategoriesBookCount();
      
      // 初始化图表
      nextTick(() => {
        initChart();
      });
    }

    // 监听窗口大小变化，调整图表大小
    window.addEventListener('resize', handleResize);
    
    // 所有数据加载完成后，处理路由参数
    nextTick(() => {
      // 延迟处理路由参数，确保组件完全加载
      setTimeout(() => {
        handleRouteParams();
      }, 300);
    });
    
  } catch (error) {
    console.error('初始化分类页面失败:', error);
    ElMessage.error('加载数据失败，请稍后重试');
  } finally {
    bookStore.loading = false;
  }
});

// 卸载时移除事件监听
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (chart.value) {
    chart.value.dispose()
  }
})

// 组件卸载前清理状态
onBeforeUnmount(() => {
  // 重置对话框状态
  showCategoryDialog.value = false;
  selectedCategory.value = null;
  categoryBooks.value = [];
})

// 处理窗口大小变化
const handleResize = () => {
  if (chart.value) {
    chart.value.resize()
  }
}

// 初始化ECharts图表
const initChart = () => {
  if (!chartRef.value) return
  
  // 初始化ECharts实例
  chart.value = echarts.init(chartRef.value)
  
  // 准备图表数据
  updateChartData()
}

// 更新图表数据
const updateChartData = () => {
  if (!chart.value) return
  
  // 处理数据 - 过滤掉数量为0的分类
  const validCategories = bookStore.categories.filter(cat => (cat.count || 0) > 0)
  const categoryNames = validCategories.map(cat => cat.name)
  const categoryCounts = validCategories.map(cat => cat.count || 0)
  
  // 定义分类对应的固定颜色
  const colorMap = {
    '历史': '#4e79a7',
    '古典文学': '#76b7b2',
    '外国文学': '#f28e2c',
    '现当代文学': '#e15759',
    '心理学': '#59a14f',
    '推理小说': '#edc949',
    '随笔': '#af7aa1',
    '文学评论': '#9c755f',
    '诗歌': '#ff9da7',
    '奇幻文学': '#bab0ab',
    '散文': '#d37295',
    '科普': '#a4a6d8',
    '计算机': '#1f77b4',
    '管理学': '#ff7f0e',
    '科幻小说': '#2ca02c'
  }
  
  // 生成饼图数据，包含值和名称
  const pieData = categoryNames.map((name, index) => ({
    value: categoryCounts[index],
    name: name,
    // 如果有预定义颜色就使用，否则使用默认颜色
    itemStyle: colorMap[name] ? { color: colorMap[name] } : {}
  }))
  
  // 设置图表选项
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} 本 ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      data: categoryNames,
      formatter: function(name) {
        // 查找该分类的数量
        const category = validCategories.find(cat => cat.name === name)
        const count = category ? category.count || 0 : 0
        // 返回格式化的图例文本
        return `${name} (${count}本)`
      }
    },
    series: [
      {
        name: '分类统计',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          position: 'outside',
          formatter: '{b}: {c}本'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '16',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: true
        },
        data: pieData
      }
    ],
    color: Object.values(colorMap) // 使用预定义的颜色列表
  }

  // 设置图表
  chart.value.setOption(option)
}

// 查看分类
const viewCategory = async (category) => {
  if (!category || !category.id) {
    console.error('无效的分类数据:', category);
    ElMessage.error('无效的分类数据');
    return;
  }

  console.log(`准备查看分类: ${category.name} (ID: ${category.id})`);
  selectedCategory.value = category;
  showCategoryDialog.value = true;
  categoryBooks.value = []; // 先清空现有数据
  
  // 加载该分类下的图书
  categoryBooksLoading.value = true;
  try {
    console.log(`加载分类ID=${category.id}的图书...`);
    const response = await categoryApi.getCategoryBooks(category.id);
    
    // 数据处理
    if (Array.isArray(response.data)) {
      console.log(`成功获取分类图书，数量: ${response.data.length}`);
      categoryBooks.value = response.data.map(book => ({
        ...book,
        price: parseFloat(book.price) || 0 // 确保价格是数字
      }));
    } else if (response.data && response.data.results) {
      console.log(`成功获取分类图书(分页)，数量: ${response.data.results.length}`);
      categoryBooks.value = response.data.results.map(book => ({
        ...book,
        price: parseFloat(book.price) || 0
      }));
    } else {
      console.warn('获取到的分类图书数据格式不正确:', response.data);
      categoryBooks.value = [];
      ElMessage.warning('获取分类图书数据格式不正确');
    }
  } catch (error) {
    console.error('获取分类图书失败:', error);
    console.error('错误详情:', error.response?.data || error.message);
    
    if (error.response?.status === 404) {
      ElMessage.error('未找到此分类或其下暂无图书');
    } else {
      ElMessage.error('获取分类图书失败，请稍后重试');
    }
    categoryBooks.value = [];
  } finally {
    categoryBooksLoading.value = false;
  }
}

// 查看图书
const viewBook = (book) => {
  if (!book || !book.id) {
    console.error('无效的图书数据:', book);
    return;
  }

  console.log(`准备查看图书: ID=${book.id}, 标题=${book.title}`);
  
  // 保存要跳转的图书ID
  const bookId = book.id;
  
  // 先关闭对话框并重置状态
  showCategoryDialog.value = false;
  selectedCategory.value = null;
  categoryBooks.value = [];
  
  // 延迟导航以确保对话框已完全关闭
  setTimeout(() => {
    console.log(`跳转到图书详情页: /book-detail?id=${bookId}`);
    router.push({
      path: '/book-detail',
      query: { id: bookId }
    });
    }, 200);
}

// 获取图书封面URL - 使用统一的工具函数
const getBookCoverUrl = (id, title) => {
  return mediaUtils.getBookCoverUrl(id, title)
}

// 处理对话框关闭事件
const handleDialogClosed = () => {
  // 清除选中的分类，避免对话框重新弹出
  selectedCategory.value = null
  categoryBooks.value = []
}

// 处理对话框关闭前的确认
const handleBeforeClose = (done) => {
  // 先置空选中的分类，避免关闭后重新打开
  selectedCategory.value = null;
  categoryBooks.value = [];
  // 继续关闭操作
  done();
}

// 处理对话框关闭按钮点击
const handleDialogClose = () => {
  showCategoryDialog.value = false;
  // 在对话框完全关闭前重置状态
  selectedCategory.value = null;
  categoryBooks.value = [];
}
</script>

<style scoped>
.category-card {
  transition: all 0.3s ease;
}

.category-card:hover {
  transform: translateY(-2px);
}
</style> 