// API 基础配置
const API_BASE_URL = 'http://127.0.0.1:8001/api';
const MEDIA_BASE_URL = 'http://127.0.0.1:8001';

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
        case 'messages':
            loadMessages();
            break;
    }
}

// 加载随机hero图片
async function loadRandomHeroImage() {
    try {
        const response = await axios.get(`${API_BASE_URL}/gallery/random-hero`);
        const heroImg = document.querySelector('#hero-image');
        if (heroImg && response.data.image_url) {
            // 构建完整的图片URL
            const imageUrl = `${API_BASE_URL.replace('/api', '')}${response.data.image_url}`;
            heroImg.src = imageUrl;
            heroImg.alt = "随机展示图片";
            console.log('Hero image loaded:', imageUrl);
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
        const featuredResponse = await axios.get(`${API_BASE_URL}/gallery/featured`);
        const timelineResponse = await axios.get(`${API_BASE_URL}/timeline/featured`);
        
        await displayFeaturedPhotos();
        displayFeaturedVideos(featuredResponse.data.videos.slice(0, 3));
        displayFeaturedEvents(timelineResponse.data.events.slice(0, 5));
        
        // 加载首页留言墙
        loadHomeMessageWall();
        
    } catch (error) {
        console.error('Error loading homepage:', error);
        showError('featured-photos', '加载失败');
        showError('featured-videos', '加载失败');
        showError('featured-events', '加载失败');
    }
}

// 加载wall-pic目录的照片
async function loadWallPhotos() {
    try {
        const response = await axios.get(`${API_BASE_URL}/gallery/wall-photos`);
        return response.data.photos || [];
    } catch (error) {
        console.error('Error loading wall photos:', error);
        return [];
    }
}

// 显示精选照片
async function displayFeaturedPhotos() {
    const container = document.getElementById('featured-photos');
    container.innerHTML = '<div class="loading">加载中...</div>';
    
    try {
        const wallPhotos = await loadWallPhotos();
        
        if (wallPhotos.length === 0) {
            container.innerHTML = '<div class="col-12"><p class="text-muted text-center">暂无照片</p></div>';
            return;
        }
        
        container.innerHTML = '';
        
        // 显示最多12张照片，创建Instagram风格的网格
        wallPhotos.slice(0, 12).forEach((photo, index) => {
            const photoElement = document.createElement('div');
            photoElement.className = 'wall-photo-item';
            photoElement.setAttribute('data-index', index);
            
            photoElement.innerHTML = `
                <img src="${MEDIA_BASE_URL}${photo.url}" alt="${photo.filename}" loading="lazy">
            `;
            
            // 添加点击事件打开lightbox
            photoElement.addEventListener('click', () => {
                // 为lightbox准备完整URL的photos数组
                const photosWithFullUrl = wallPhotos.map(p => ({
                    ...p,
                    url: MEDIA_BASE_URL + p.url
                }));
                openLightbox(photosWithFullUrl, index);
            });
            
            container.appendChild(photoElement);
        });
        
    } catch (error) {
        console.error('Error displaying featured photos:', error);
        container.innerHTML = '<div class="alert alert-danger">加载照片失败</div>';
    }
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
        
        let url = `${API_BASE_URL}/gallery/photos?skip=${(page-1)*20}&limit=20`;
        if (category) {
            url += `&category=${category}`;
        }
        
        const response = await axios.get(url);
        displayPhotos(response.data);
        // FastAPI返回的是直接的数组，没有分页信息暂时注释
        // displayPagination(response.data, 'photos', loadPhotos);
        
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
        
        let url = `${API_BASE_URL}/gallery/videos?skip=${(page-1)*20}&limit=20`;
        if (category) {
            url += `&category=${category}`;
        }
        
        const response = await axios.get(url);
        displayVideos(response.data);
        // FastAPI返回的是直接的数组，没有分页信息暂时注释
        // displayPagination(response.data, 'videos', loadVideos);
        
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
        
        let url = `${API_BASE_URL}/timeline/events`;
        if (featured === 'featured') {
            url += '?is_featured=true';
        }
        
        const response = await axios.get(url);
        displayTimeline(response.data);
        
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

// Lightbox 功能
let currentLightboxPhotos = [];
let currentLightboxIndex = 0;

function createLightbox() {
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.innerHTML = `
        <div class="lightbox-content">
            <span class="lightbox-close">&times;</span>
            <img class="lightbox-image" src="" alt="">
            <span class="lightbox-nav prev">&#10094;</span>
            <span class="lightbox-nav next">&#10095;</span>
            <div class="lightbox-counter"><span class="current">1</span> / <span class="total">1</span></div>
        </div>
    `;
    
    document.body.appendChild(lightbox);
    
    // 事件监听器
    lightbox.querySelector('.lightbox-close').addEventListener('click', closeLightbox);
    lightbox.querySelector('.lightbox-nav.prev').addEventListener('click', showPrevPhoto);
    lightbox.querySelector('.lightbox-nav.next').addEventListener('click', showNextPhoto);
    
    // 点击背景关闭
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) {
            closeLightbox();
        }
    });
    
    // 键盘导航
    document.addEventListener('keydown', handleLightboxKeyboard);
    
    return lightbox;
}

function openLightbox(photos, index) {
    currentLightboxPhotos = photos;
    currentLightboxIndex = index;
    
    let lightbox = document.querySelector('.lightbox');
    if (!lightbox) {
        lightbox = createLightbox();
    }
    
    updateLightboxPhoto();
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    const lightbox = document.querySelector('.lightbox');
    if (lightbox) {
        lightbox.classList.remove('active');
        document.body.style.overflow = '';
    }
}

function showPrevPhoto() {
    currentLightboxIndex = (currentLightboxIndex - 1 + currentLightboxPhotos.length) % currentLightboxPhotos.length;
    updateLightboxPhoto();
}

function showNextPhoto() {
    currentLightboxIndex = (currentLightboxIndex + 1) % currentLightboxPhotos.length;
    updateLightboxPhoto();
}

function updateLightboxPhoto() {
    const lightbox = document.querySelector('.lightbox');
    if (!lightbox || !currentLightboxPhotos[currentLightboxIndex]) return;
    
    const photo = currentLightboxPhotos[currentLightboxIndex];
    const img = lightbox.querySelector('.lightbox-image');
    const counter = lightbox.querySelector('.lightbox-counter');
    
    img.src = photo.url;
    img.alt = photo.filename;
    
    counter.querySelector('.current').textContent = currentLightboxIndex + 1;
    counter.querySelector('.total').textContent = currentLightboxPhotos.length;
    
    // 更新导航按钮可见性
    const prevBtn = lightbox.querySelector('.lightbox-nav.prev');
    const nextBtn = lightbox.querySelector('.lightbox-nav.next');
    
    if (currentLightboxPhotos.length <= 1) {
        prevBtn.style.display = 'none';
        nextBtn.style.display = 'none';
    } else {
        prevBtn.style.display = 'flex';
        nextBtn.style.display = 'flex';
    }
}

function handleLightboxKeyboard(e) {
    const lightbox = document.querySelector('.lightbox');
    if (!lightbox || !lightbox.classList.contains('active')) return;
    
    switch(e.key) {
        case 'Escape':
            closeLightbox();
            break;
        case 'ArrowLeft':
            showPrevPhoto();
            break;
        case 'ArrowRight':
            showNextPhoto();
            break;
    }
}

// 显示照片模态框（保持向后兼容）
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
    
    // 留言板事件监听
    setupMessageBoardEvents();
});

// 留言板功能
function setupMessageBoardEvents() {
    // 留言表单提交
    const messageForm = document.getElementById('message-form');
    if (messageForm) {
        messageForm.addEventListener('submit', submitMessage);
        
        // 字数统计
        const contentTextarea = document.getElementById('message-content');
        const charCounter = document.querySelector('.char-counter');
        if (contentTextarea && charCounter) {
            contentTextarea.addEventListener('input', function() {
                const currentLength = this.value.length;
                charCounter.textContent = `${currentLength} / 2000`;
                
                if (currentLength > 1900) {
                    charCounter.style.color = '#ef4444';
                } else {
                    charCounter.style.color = 'var(--warm-brown)';
                }
            });
        }
    }
}

// 加载留言板页面
async function loadMessages() {
    try {
        await Promise.all([
            loadMessageStats(),
            loadApprovedMessages()
        ]);
    } catch (error) {
        console.error('Error loading messages page:', error);
    }
}

// 加载留言统计
async function loadMessageStats() {
    try {
        const response = await axios.get(`${API_BASE_URL}/messages/stats`);
        displayMessageStats(response.data);
    } catch (error) {
        console.error('Error loading message stats:', error);
    }
}

// 显示留言统计
function displayMessageStats(stats) {
    const container = document.getElementById('message-stats');
    if (!container) return;
    
    container.innerHTML = `
        <div class="stats-item">
            <div class="stats-number">${stats.approved_messages}</div>
            <div class="stats-label">已发布留言</div>
        </div>
        <div class="stats-item">
            <div class="stats-number">${stats.pending_messages}</div>
            <div class="stats-label">等待审核</div>
        </div>
        <div class="stats-item">
            <div class="stats-number">${stats.total_messages}</div>
            <div class="stats-label">总留言数</div>
        </div>
    `;
}

// 加载已审核留言
async function loadApprovedMessages(page = 1) {
    try {
        showLoading('messages-container');
        
        const response = await axios.get(`${API_BASE_URL}/messages?skip=${(page-1)*20}&limit=20`);
        displayMessages(response.data);
        
    } catch (error) {
        console.error('Error loading messages:', error);
        showError('messages-container', '加载留言失败');
    }
}

// 显示留言
function displayMessages(messages) {
    const container = document.getElementById('messages-container');
    if (!container) return;
    
    if (!messages || messages.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">💬</div>
                <p>还没有留言哦，快来留下第一条留言吧！</p>
            </div>
        `;
        return;
    }
    
    const html = messages.map(message => `
        <div class="message-item">
            <div class="message-header">
                <div class="message-nickname">${escapeHtml(message.nickname)}</div>
                <div class="message-date">${formatDateTime(message.created_at)}</div>
            </div>
            <div class="message-content">${escapeHtml(message.content)}</div>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

// 提交留言
async function submitMessage(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const submitBtn = form.querySelector('.submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoading = submitBtn.querySelector('.btn-loading');
    
    // 获取表单数据
    const messageData = {
        nickname: formData.get('nickname').trim(),
        content: formData.get('content').trim(),
        email: formData.get('email').trim()
    };
    
    // 基本验证
    if (!messageData.nickname || !messageData.content) {
        showAlert('请填写昵称和留言内容', 'danger');
        return;
    }
    
    if (messageData.nickname.length > 50) {
        showAlert('昵称最多50个字符', 'danger');
        return;
    }
    
    if (messageData.content.length > 2000) {
        showAlert('留言内容最多2000个字符', 'danger');
        return;
    }
    
    // 显示加载状态
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline-flex';
    
    try {
        const response = await axios.post(`${API_BASE_URL}/messages`, messageData);
        
        if (response.data.status === 'pending') {
            showAlert('留言已提交，等待审核后显示。感谢你的留言！ 🌸', 'success');
            form.reset();
            document.querySelector('.char-counter').textContent = '0 / 2000';
            // 刷新统计
            loadMessageStats();
        } else {
            showAlert(response.data.message, 'warning');
        }
        
    } catch (error) {
        console.error('Error submitting message:', error);
        
        if (error.response?.status === 429) {
            showAlert('提交太频繁，请稍后再试', 'warning');
        } else if (error.response?.data?.detail) {
            showAlert(error.response.data.detail, 'danger');
        } else {
            showAlert('提交失败，请稍后重试', 'danger');
        }
    } finally {
        // 恢复按钮状态
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    }
}

// 显示提示消息
function showAlert(message, type = 'info') {
    // 移除已存在的alert
    const existingAlert = document.querySelector('.message-form-section .alert');
    if (existingAlert) {
        existingAlert.remove();
    }
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const formSection = document.querySelector('.message-form-section');
    if (formSection) {
        formSection.insertBefore(alertDiv, formSection.firstChild);
        
        // 3秒后自动消失
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// HTML转义函数
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 格式化日期时间
function formatDateTime(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return dateString;
    
    const now = new Date();
    const diff = now - date;
    const hours = diff / (1000 * 60 * 60);
    
    if (hours < 1) {
        const minutes = Math.floor(diff / (1000 * 60));
        return minutes <= 0 ? '刚刚' : `${minutes}分钟前`;
    } else if (hours < 24) {
        return `${Math.floor(hours)}小时前`;
    } else if (hours < 24 * 7) {
        return `${Math.floor(hours / 24)}天前`;
    } else {
        return date.toLocaleDateString('zh-CN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }
}

// ===== 首页留言墙功能 =====

// 加载首页留言墙
async function loadHomeMessageWall() {
    const container = document.getElementById('home-message-wall');
    if (!container) return;
    
    try {
        container.innerHTML = '<div class="message-wall-loading">加载留言中...</div>';
        
        // 获取最近的10条留言
        const response = await axios.get(`${API_BASE_URL}/messages?skip=0&limit=10`);
        const messages = response.data || [];
        
        if (messages.length === 0) {
            container.innerHTML = `
                <div class="message-wall-empty">
                    <div class="message-wall-empty-icon">💭</div>
                    <p>还没有留言呢，快去留言板留下第一条留言吧！</p>
                </div>
            `;
            return;
        }
        
        // 创建贴纸样式的留言
        const stickyNotes = messages.map((message, index) => {
            const position = generateStickyPosition(index, container);
            const colorClass = `color-${(index % 5) + 1}`;
            
            return `
                <div class="sticky-note ${colorClass}" 
                     style="top: ${position.top}px; left: ${position.left}px;" 
                     onclick="showPage('messages')"
                     title="点击查看更多留言">
                    <div class="sticky-note-header">
                        <div class="sticky-note-name">${escapeHtml(message.nickname)}</div>
                        <div class="sticky-note-date">${formatRelativeTime(message.created_at)}</div>
                    </div>
                    <div class="sticky-note-content">${escapeHtml(truncateText(message.content, 60))}</div>
                </div>
            `;
        }).join('');
        
        container.innerHTML = stickyNotes;
        
    } catch (error) {
        console.error('Error loading home message wall:', error);
        container.innerHTML = `
            <div class="message-wall-empty">
                <div class="message-wall-empty-icon">❌</div>
                <p>加载留言失败，请稍后再试</p>
            </div>
        `;
    }
}

// 生成贴纸位置（避免重叠）
function generateStickyPosition(index, container) {
    const containerWidth = container.clientWidth || 800;
    const containerHeight = 400;
    const noteWidth = 180;
    const noteHeight = 120;
    
    // 计算每行能放几个贴纸
    const notesPerRow = Math.floor((containerWidth - 40) / (noteWidth + 20));
    const maxRows = Math.floor(containerHeight / (noteHeight + 20));
    
    const row = Math.floor(index / notesPerRow);
    const col = index % notesPerRow;
    
    // 如果超出容器范围，则随机放置
    if (row >= maxRows) {
        return {
            top: Math.random() * (containerHeight - noteHeight - 40) + 20,
            left: Math.random() * (containerWidth - noteWidth - 40) + 20
        };
    }
    
    // 基础位置
    let baseTop = row * (noteHeight + 20) + 20;
    let baseLeft = col * (noteWidth + 20) + 20;
    
    // 添加随机偏移，让贴纸看起来更自然
    const randomOffsetTop = (Math.random() - 0.5) * 30;
    const randomOffsetLeft = (Math.random() - 0.5) * 40;
    
    return {
        top: Math.max(10, Math.min(containerHeight - noteHeight - 10, baseTop + randomOffsetTop)),
        left: Math.max(10, Math.min(containerWidth - noteWidth - 10, baseLeft + randomOffsetLeft))
    };
}

// 格式化相对时间
function formatRelativeTime(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    
    const minute = 60 * 1000;
    const hour = minute * 60;
    const day = hour * 24;
    const week = day * 7;
    const month = day * 30;
    
    if (diff < minute) {
        return '刚刚';
    } else if (diff < hour) {
        return `${Math.floor(diff / minute)}分钟前`;
    } else if (diff < day) {
        return `${Math.floor(diff / hour)}小时前`;
    } else if (diff < week) {
        return `${Math.floor(diff / day)}天前`;
    } else if (diff < month) {
        return `${Math.floor(diff / week)}周前`;
    } else {
        return `${Math.floor(diff / month)}个月前`;
    }
}

// 截断文本
function truncateText(text, maxLength) {
    if (text.length <= maxLength) {
        return text;
    }
    return text.substring(0, maxLength) + '...';
}

// ===== 留言墙设计方案切换 =====

// 切换留言墙设计方案（开发用，可以在控制台调用）
function switchMessageWallStyle(style) {
    const container = document.getElementById('home-message-wall');
    if (!container) return;
    
    // 移除现有样式类
    container.classList.remove('graffiti-style', 'minimal-style');
    
    // 添加新样式类
    if (style === 'graffiti') {
        container.classList.add('graffiti-style');
        loadHomeMessageWallGraffiti();
    } else if (style === 'minimal') {
        container.classList.add('minimal-style');
        loadHomeMessageWallMinimal();
    } else {
        // 默认贴纸风格
        loadHomeMessageWall();
    }
}

// 涂鸦墙风格的留言加载
async function loadHomeMessageWallGraffiti() {
    const container = document.getElementById('home-message-wall');
    if (!container) return;
    
    try {
        container.innerHTML = '<div class="message-wall-loading">加载留言中...</div>';
        
        const response = await axios.get(`${API_BASE_URL}/messages?skip=0&limit=8`);
        const messages = response.data || [];
        
        if (messages.length === 0) {
            container.innerHTML = `
                <div class="message-wall-empty">
                    <div class="message-wall-empty-icon">🎨</div>
                    <p>涂鸦墙还是空白的，快来画下第一笔吧！</p>
                </div>
            `;
            return;
        }
        
        const graffitiMessages = messages.map((message, index) => {
            const position = generateStickyPosition(index, container);
            
            return `
                <div class="graffiti-message" 
                     style="top: ${position.top}px; left: ${position.left}px;"
                     onclick="showPage('messages')"
                     title="点击查看更多留言">
                    <strong>${escapeHtml(message.nickname)}:</strong><br>
                    ${escapeHtml(truncateText(message.content, 50))}
                </div>
            `;
        }).join('');
        
        container.innerHTML = graffitiMessages;
        
    } catch (error) {
        console.error('Error loading graffiti message wall:', error);
    }
}

// 简约卡片风格的留言加载
async function loadHomeMessageWallMinimal() {
    const container = document.getElementById('home-message-wall');
    if (!container) return;
    
    try {
        container.innerHTML = '<div class="message-wall-loading">加载留言中...</div>';
        
        const response = await axios.get(`${API_BASE_URL}/messages?skip=0&limit=6`);
        const messages = response.data || [];
        
        if (messages.length === 0) {
            container.innerHTML = `
                <div class="message-wall-empty">
                    <div class="message-wall-empty-icon">📝</div>
                    <p>留言区域还很安静，期待你的声音...</p>
                </div>
            `;
            return;
        }
        
        const minimalMessages = messages.map(message => `
            <div class="minimal-message" onclick="showPage('messages')" title="点击查看更多留言">
                <div class="message-header">
                    <div class="message-nickname">${escapeHtml(message.nickname)}</div>
                    <div class="message-date">${formatRelativeTime(message.created_at)}</div>
                </div>
                <div class="message-content">${escapeHtml(truncateText(message.content, 100))}</div>
            </div>
        `).join('');
        
        container.innerHTML = minimalMessages;
        
    } catch (error) {
        console.error('Error loading minimal message wall:', error);
    }
}