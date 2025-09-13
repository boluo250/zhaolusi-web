// API 基础配置
const API_BASE_URL = 'http://127.0.0.1:8001/api';

// 页面导航
function showPage(pageName) {
    // 隐藏所有页面
    document.querySelectorAll('.page').forEach(page => {
        page.style.display = 'none';
    });
    
    // 显示目标页面
    document.getElementById(pageName + '-page').style.display = 'block';
    
    // 根据页面加载数据
    switch(pageName) {
        case 'home':
            loadHomepage();
            break;
        case 'photos':
            loadPhotos();
            break;
        case 'videos':
            loadVideos();
            break;
        case 'timeline':
            loadTimeline();
            break;
    }
}

// 加载随机hero图片
async function loadRandomHeroImage() {
    try {
        const response = await axios.get(`${API_BASE_URL}/gallery/random-hero/`);
        const heroImg = document.querySelector('.hero-image img');
        if (heroImg && response.data.image_url) {
            // 构建完整的URL，使用后端服务器地址
            const baseUrl = API_BASE_URL.replace('/api', '');  // http://127.0.0.1:8001
            const imageUrl = baseUrl + response.data.image_url;
            heroImg.src = imageUrl;
            heroImg.alt = "随机展示图片";
        }
    } catch (error) {
        console.error('Error loading random hero image:', error);
        // 如果加载失败，保持原有的占位图片
    }
}

// 加载首页数据
async function loadHomepage() {
    try {
        showLoading('featured-photos');
        showLoading('featured-videos');
        showLoading('featured-events');
        
        // 加载随机hero图片
        await loadRandomHeroImage();
        
        // 加载精选内容
        const featuredResponse = await axios.get(`${API_BASE_URL}/gallery/featured/`);
        const timelineResponse = await axios.get(`${API_BASE_URL}/timeline/featured/`);
        
        displayFeaturedPhotos(featuredResponse.data.photos.slice(0, 6));
        displayFeaturedVideos(featuredResponse.data.videos.slice(0, 3));
        displayFeaturedEvents(timelineResponse.data.events.slice(0, 5));
        
    } catch (error) {
        console.error('Error loading homepage:', error);
        showError('featured-photos', '加载失败');
        showError('featured-videos', '加载失败');
        showError('featured-events', '加载失败');
    }
}

// 显示精选照片
function displayFeaturedPhotos(photos) {
    const container = document.getElementById('featured-photos');
    
    // 使用示例数据如果没有真实数据
    if (!photos || photos.length === 0) {
        photos = [
            { id: 1, title: '春日遊記', file_path: 'https://picsum.photos/600/400?random=1', description: '温暖的午后时光' },
            { id: 2, title: '城市印象', file_path: 'https://picsum.photos/300/200?random=2', description: '城市的繁华与宁静' },
            { id: 3, title: '自然之美', file_path: 'https://picsum.photos/300/200?random=3', description: '大自然的鬼斧神工' },
            { id: 4, title: '午後時光', file_path: 'https://picsum.photos/200/200?random=4', description: '慵懒的下午' },
            { id: 5, title: '夜景', file_path: 'https://picsum.photos/200/200?random=5', description: '城市夜晚的灯火' }
        ];
    }
    
    container.innerHTML = '';
    
    photos.slice(0, 5).forEach((photo, index) => {
        const photoElement = document.createElement('div');
        photoElement.className = index === 0 ? 'photo-large' : (index < 3 ? 'photo-medium' : 'photo-small');
        
        const imageUrl = photo.file_path.startsWith('http') ? photo.file_path : `${API_BASE_URL.replace('/api', '')}${photo.file_path}`;
        
        photoElement.innerHTML = `
            <img src="${imageUrl}" alt="${photo.title}" onclick="showPhotoModal(${photo.id}, '${photo.title}', '${imageUrl}', '${photo.description || ''}')">
            ${index < 3 ? `<div class="photo-overlay"><h4>${photo.title}</h4><p>${photo.description || ''}</p></div>` : ''}
        `;
        
        container.appendChild(photoElement);
    });
}

// 显示精选视频
function displayFeaturedVideos(videos) {
    const container = document.getElementById('featured-videos');
    
    // 使用示例数据如果没有真实数据
    if (!videos || videos.length === 0) {
        videos = [
            { id: 1, title: '一段美好的旅程', thumbnail: 'https://picsum.photos/400/200?random=6', description: '这是一次难忘的旅行，让我们一起回顾那些美好的瞬间' }
        ];
    }
    
    const video = videos[0];
    const imageUrl = video.thumbnail && video.thumbnail.startsWith('http') ? video.thumbnail : 
                     video.thumbnail ? `${API_BASE_URL.replace('/api', '')}${video.thumbnail}` : 
                     'https://picsum.photos/400/200?random=6';
    
    container.innerHTML = `
        <div class="video-featured">
            <img src="${imageUrl}" alt="${video.title}">
            <h4 class="video-title">${video.title}</h4>
            <p class="video-description">${video.description || '动态的记忆更能触动心弦，这里收集了生活中的精彩影像片段。'}</p>
        </div>
    `;
}

// 显示精选事件
function displayFeaturedEvents(events) {
    const container = document.getElementById('featured-events');
    
    // 使用示例数据如果没有真实数据
    if (!events || events.length === 0) {
        events = [
            { id: 1, title: '完成重要项目', description: '经过几个月的努力，终于完成了这个对我来说很重要的项目。', event_date: '2024-03-15' },
            { id: 2, title: '独自旅行', description: '第一次一个人的旅行，收获了很多意想不到的美好。', event_date: '2024-01-10' },
            { id: 3, title: '新的开始', description: '开始了新的工作，迎来人生的新阶段。', event_date: '2023-12-01' }
        ];
    }
    
    container.innerHTML = '';
    
    events.slice(0, 3).forEach(event => {
        const eventElement = document.createElement('div');
        eventElement.className = 'timeline-item';
        
        eventElement.innerHTML = `
            <div class="timeline-date">${formatDate(event.event_date)}</div>
            <div class="timeline-content">
                <h5 class="timeline-title">${event.title}</h5>
                <p class="timeline-desc">${event.description}</p>
            </div>
        `;
        
        container.appendChild(eventElement);
    });
}

// 加载照片页面
async function loadPhotos(page = 1, category = '') {
    try {
        showLoading('photos-grid');
        
        let url = `${API_BASE_URL}/gallery/photos/?page=${page}`;
        if (category) {
            url += `&category=${category}`;
        }
        
        const response = await axios.get(url);
        displayPhotos(response.data.results);
        displayPagination(response.data, 'photos', loadPhotos);
        
    } catch (error) {
        console.error('Error loading photos:', error);
        showError('photos-grid', '加载照片失败');
    }
}

// 显示照片
function displayPhotos(photos) {
    const container = document.getElementById('photos-grid');
    
    if (!photos || photos.length === 0) {
        container.innerHTML = '<div class="col-12"><p class="text-muted text-center">暂无照片</p></div>';
        return;
    }
    
    const html = photos.map(photo => `
        <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
            <div class="card photo-card" onclick="showPhotoModal(${photo.id}, '${photo.title}', '${photo.file_path}', '${photo.description || ''}')">
                <img src="${API_BASE_URL.replace('/api', '')}${photo.file_path}" class="card-img-top" alt="${photo.title}">
                <div class="card-body">
                    <h6 class="card-title">${photo.title}</h6>
                    <p class="card-text"><small class="text-muted">${getCategoryName(photo.category)}</small></p>
                </div>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

// 加载视频页面
async function loadVideos(page = 1, category = '') {
    try {
        showLoading('videos-grid');
        
        let url = `${API_BASE_URL}/gallery/videos/?page=${page}`;
        if (category) {
            url += `&category=${category}`;
        }
        
        const response = await axios.get(url);
        displayVideos(response.data.results);
        displayPagination(response.data, 'videos', loadVideos);
        
    } catch (error) {
        console.error('Error loading videos:', error);
        showError('videos-grid', '加载视频失败');
    }
}

// 显示视频
function displayVideos(videos) {
    const container = document.getElementById('videos-grid');
    
    if (!videos || videos.length === 0) {
        container.innerHTML = '<div class="col-12"><p class="text-muted text-center">暂无视频</p></div>';
        return;
    }
    
    const html = videos.map(video => `
        <div class="col-lg-4 col-md-6 mb-4">
            <div class="card video-card">
                ${video.thumbnail ? 
                    `<img src="${API_BASE_URL.replace('/api', '')}${video.thumbnail}" class="card-img-top" alt="${video.title}">` :
                    '<div class="card-img-top bg-secondary d-flex align-items-center justify-content-center" style="height: 200px;"><i class="fas fa-play fa-3x text-white"></i></div>'
                }
                <div class="card-body">
                    <h6 class="card-title">${video.title}</h6>
                    <p class="card-text">${video.description || ''}</p>
                    <p class="card-text"><small class="text-muted">${getCategoryName(video.category)}</small></p>
                    ${video.embed_link ? `<a href="${video.embed_link}" target="_blank" class="btn btn-primary btn-sm">观看视频</a>` : ''}
                </div>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

// 加载时间轴
async function loadTimeline(featured = '') {
    try {
        showLoading('timeline-events');
        
        let url = `${API_BASE_URL}/timeline/events/`;
        if (featured === 'featured') {
            url += '?is_featured=true';
        }
        
        const response = await axios.get(url);
        displayTimeline(response.data.results);
        
    } catch (error) {
        console.error('Error loading timeline:', error);
        showError('timeline-events', '加载时间轴失败');
    }
}

// 显示时间轴
function displayTimeline(events) {
    const container = document.getElementById('timeline-events');
    
    if (!events || events.length === 0) {
        container.innerHTML = '<p class="text-muted text-center">暂无事件</p>';
        return;
    }
    
    const html = `
        <div class="timeline">
            ${events.map(event => `
                <div class="timeline-item ${event.is_featured ? 'timeline-featured' : ''}">
                    <div class="timeline-card">
                        <h5>${event.title}</h5>
                        <p class="text-muted mb-2">${formatDate(event.event_date)} ${event.location ? '· ' + event.location : ''}</p>
                        <p>${event.description}</p>
                        ${event.image ? `<img src="${API_BASE_URL.replace('/api', '')}${event.image}" class="img-fluid rounded mt-2" alt="${event.title}">` : ''}
                        <span class="badge bg-primary">${getEventTypeName(event.event_type)}</span>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
    
    container.innerHTML = html;
}

// 显示照片模态框
function showPhotoModal(id, title, imagePath, description) {
    document.getElementById('photoModalTitle').textContent = title;
    document.getElementById('photoModalImage').src = API_BASE_URL.replace('/api', '') + imagePath;
    document.getElementById('photoModalDescription').textContent = description || '';
    
    const modal = new bootstrap.Modal(document.getElementById('photoModal'));
    modal.show();
}

// 显示分页
function displayPagination(data, type, loadFunction) {
    const container = document.getElementById(type + '-pagination');
    
    if (!data.previous && !data.next) {
        container.innerHTML = '';
        return;
    }
    
    const currentPage = Math.ceil((data.count - data.results.length) / 20) + 1;
    const totalPages = Math.ceil(data.count / 20);
    
    let html = '<nav><ul class="pagination">';
    
    // 上一页
    if (data.previous) {
        html += `<li class="page-item"><a class="page-link" href="#" onclick="${loadFunction.name}(${currentPage - 1}, getFilterValue('${type}'))">上一页</a></li>`;
    }
    
    // 页码
    for (let i = Math.max(1, currentPage - 2); i <= Math.min(totalPages, currentPage + 2); i++) {
        html += `<li class="page-item ${i === currentPage ? 'active' : ''}"><a class="page-link" href="#" onclick="${loadFunction.name}(${i}, getFilterValue('${type}'))">${i}</a></li>`;
    }
    
    // 下一页
    if (data.next) {
        html += `<li class="page-item"><a class="page-link" href="#" onclick="${loadFunction.name}(${currentPage + 1}, getFilterValue('${type}'))">下一页</a></li>`;
    }
    
    html += '</ul></nav>';
    container.innerHTML = html;
}

// 工具函数
function showLoading(containerId) {
    document.getElementById(containerId).innerHTML = '<div class="loading">加载中...</div>';
}

function showError(containerId, message) {
    document.getElementById(containerId).innerHTML = `<div class="alert alert-danger">${message}</div>`;
}

function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    if (isNaN(date.getTime())) {
        // 如果解析失败，尝试直接返回原始字符串
        return dateString;
    }
    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'short'
    });
}

function getCategoryName(category) {
    const categories = {
        'travel': '旅行',
        'family': '家人',
        'life': '生活',
        'work': '工作',
        'other': '其他'
    };
    return categories[category] || category;
}

function getEventTypeName(eventType) {
    const types = {
        'milestone': '人生里程碑',
        'achievement': '成就',
        'travel': '旅行',
        'work': '工作',
        'education': '教育',
        'family': '家庭',
        'other': '其他'
    };
    return types[eventType] || eventType;
}

function getFilterValue(type) {
    const filterId = type.slice(0, -1) + '-category-filter';  // photos -> photo-category-filter
    const element = document.getElementById(filterId);
    return element ? element.value : '';
}

// 事件监听器
document.addEventListener('DOMContentLoaded', function() {
    // 确保首页可见
    showPage('home');
    
    // 分类筛选事件
    const photoFilter = document.getElementById('photo-category-filter');
    if (photoFilter) {
        photoFilter.addEventListener('change', function() {
            loadPhotos(1, this.value);
        });
    }
    
    const videoFilter = document.getElementById('video-category-filter');
    if (videoFilter) {
        videoFilter.addEventListener('change', function() {
            loadVideos(1, this.value);
        });
    }
    
    const timelineFilter = document.getElementById('timeline-filter');
    if (timelineFilter) {
        timelineFilter.addEventListener('change', function() {
            loadTimeline(this.value);
        });
    }
});