<template>
  <div class="home-container">

    <!-- 英雄区域 -->
    <section class="hero-section">
      <div class="hero-content">
        <div class="logo-container">
          <span class="logo-icon">🔐</span>
          <h1 class="logo-text">密码虚拟攻防平台</h1>
        </div>
        <h2 class="hero-title">
          面向未来的
          <span class="security-text">密码学</span>
        </h2>
        <p class="hero-description">
          专注于密码学安全的攻防演练平台，提供多种密码学攻击场景和防御措施，
          帮助安全专业人员提升技能，构建更安全的网络环境。
        </p>
        <div class="hero-buttons">
          <a href="#/attack/dashboard" class="btn primary-btn">进入攻击端</a>
          <a href="#/defense/dashboard" class="btn secondary-btn">进入防御端</a>
        </div>
      </div>
    </section>

    <!-- 功能模块 -->
    <section class="features-section">
      <div class="features-content">
        <div class="feature-item">
          <div class="feature-icon">🔐</div>
          <h3 class="feature-title">密码学基础</h3>
          <p class="feature-description">了解密码学基础原理和核心概念</p>
        </div>
        <div class="feature-item">
          <div class="feature-icon">📚</div>
          <h3 class="feature-title">密码学学习路径</h3>
          <p class="feature-description">从基础到进阶，系统学习密码学</p>
        </div>
        <div class="feature-item">
          <div class="feature-icon">🛡️</div>
          <h3 class="feature-title">密码防御技术</h3>
          <p class="feature-description">学习最新的密码防御技术和方法</p>
        </div>
        <div class="feature-item">
          <div class="feature-icon">🧪</div>
          <h3 class="feature-title">密码学实验平台</h3>
          <p class="feature-description">动手实践密码学攻防技术和应用</p>
        </div>
      </div>
    </section>

    <!-- 密码学职业体系 -->
    <section class="career-section">
      <div class="career-content">
        <h2 class="section-title">密码学职业体系</h2>
        <p class="section-subtitle">由浅入深，循序渐进，进入密码学专业领域</p>
        <div class="career-cards">
          <div class="career-card">
            <div class="card-icon">🔐</div>
            <h4 class="card-title">密码学工程师</h4>
            <p class="card-description">Cryptography, Algorithm Design, Security Protocols</p>
          </div>
          <div class="career-card">
            <div class="card-icon">💻</div>
            <h4 class="card-title">安全开发工程师</h4>
            <p class="card-description">Security Coding, Cryptography, Key Management</p>
          </div>
          <div class="career-card">
            <div class="card-icon">🔍</div>
            <h4 class="card-title">密码分析专家</h4>
            <p class="card-description">Cryptanalysis, Vulnerability Assessment, Attack Techniques</p>
          </div>
          <div class="career-card">
            <div class="card-icon">🛡️</div>
            <h4 class="card-title">安全架构师</h4>
            <p class="card-description">Security Architecture, Protocol Design, Risk Assessment</p>
          </div>
          <div class="career-card">
            <div class="card-icon">📝</div>
            <h4 class="card-title">密码学研究员</h4>
            <p class="card-description">Algorithm Development, Research, Academic Publishing</p>
          </div>
        </div>
        <!-- 统计数据 -->
        <div class="stats-section">
          <div class="stat-item">
            <div class="stat-number">50+</div>
            <div class="stat-label">密码学实验室</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">80+</div>
            <div class="stat-label">密码算法</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">5000+</div>
            <div class="stat-label">注册用户</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">98%</div>
            <div class="stat-label">用户满意度</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 底部 -->
    <footer class="home-footer">
      <div class="footer-content">
        <div class="footer-info">
          <div class="footer-logo">
            <span class="logo-icon">🔐</span>
            <span class="logo-text">密码虚拟攻防平台</span>
          </div>
          <p class="footer-description">
            专注于密码学安全的攻防演练平台，提供多种密码学攻击场景和防御措施，
            帮助安全专业人员提升技能，构建更安全的网络环境。
          </p>
        </div>
        <div class="footer-links">
          <div class="link-group">
            <h4 class="link-title">平台功能</h4>
            <a href="#/attack/scenarios" class="footer-link">攻防场景</a>
            <a href="#/attack/simulate" class="footer-link">靶场演练</a>
            <a href="#/attack/training" class="footer-link">在线学习</a>
            <a href="#/attack/reports" class="footer-link">报告分析</a>
          </div>
          <div class="link-group">
            <h4 class="link-title">关于我们</h4>
            <a href="#" class="footer-link">平台介绍</a>
            <a href="#" class="footer-link">联系我们</a>
            <a href="#" class="footer-link">隐私政策</a>
            <a href="#" class="footer-link">使用条款</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p class="copyright">© 2026 密码虚拟攻防平台. 保留所有权利.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
// 首页组件逻辑
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background-color: #1a1a1a;
  color: #e0e0e0;
  font-family: 'Microsoft YaHei', Arial, sans-serif;
}

/* 英雄区域 */
.hero-section {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding: 120px 0;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 50%;
  height: 100%;
  background: radial-gradient(circle, rgba(0, 170, 255, 0.1) 0%, transparent 70%);
}

.hero-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 30px;
  position: relative;
  z-index: 1;
  text-align: center;
}

.logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  margin-bottom: 30px;
}

.logo-icon {
  font-size: 48px;
  color: #00aaff;
}

.logo-text {
  font-size: 32px;
  font-weight: bold;
  color: #e0e0e0;
}

.hero-title {
  font-size: 48px;
  font-weight: bold;
  margin-bottom: 20px;
  line-height: 1.2;
}

.security-text {
  display: block;
  color: #00aaff;
  margin-top: 10px;
}

.hero-description {
  font-size: 18px;
  line-height: 1.6;
  margin-bottom: 60px;
  max-width: 700px;
  color: #b0b0b0;
  margin-left: auto;
  margin-right: auto;
}

.hero-buttons {
  display: flex;
  gap: 30px;
  justify-content: center;
  margin-bottom: 60px;
}

.btn {
  padding: 16px 40px;
  border-radius: 6px;
  text-decoration: none;
  font-size: 18px;
  font-weight: bold;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
  min-width: 200px;
}

.primary-btn {
  background: linear-gradient(135deg, #00aaff 0%, #0066cc 100%);
  color: white;
}

.primary-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0, 170, 255, 0.4);
}

.secondary-btn {
  background-color: transparent;
  color: #00aaff;
  border: 2px solid #00aaff;
}

.secondary-btn:hover {
  background-color: rgba(0, 170, 255, 0.1);
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0, 170, 255, 0.2);
}

/* 功能模块 */
.features-section {
  background-color: #161616;
  padding: 100px 0;
}

.features-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 30px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
}

.feature-item {
  background-color: #1a1a1a;
  padding: 40px 30px;
  border-radius: 8px;
  text-align: center;
  transition: all 0.3s ease;
  border: 1px solid #2a2a2a;
}

.feature-item:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 25px rgba(0, 170, 255, 0.15);
  border-color: #00aaff;
}

.feature-icon {
  font-size: 56px;
  margin-bottom: 25px;
  color: #00aaff;
}

.feature-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #e0e0e0;
}

.feature-description {
  font-size: 16px;
  color: #b0b0b0;
  line-height: 1.6;
}

/* 职业体系 */
.career-section {
  background-color: #1a1a1a;
  padding: 100px 0;
}

.career-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 30px;
}

.section-title {
  font-size: 36px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
  color: #e0e0e0;
}

.section-subtitle {
  text-align: center;
  font-size: 18px;
  color: #b0b0b0;
  margin-bottom: 60px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.career-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 30px;
  margin-bottom: 80px;
}

.career-card {
  background-color: #161616;
  padding: 40px 30px;
  border-radius: 8px;
  text-align: center;
  transition: all 0.3s ease;
  border: 1px solid #2a2a2a;
}

.career-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 25px rgba(0, 170, 255, 0.15);
  border-color: #00aaff;
}

.card-icon {
  font-size: 48px;
  margin-bottom: 20px;
  color: #00aaff;
}

.card-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #e0e0e0;
}

.card-description {
  font-size: 14px;
  color: #b0b0b0;
  line-height: 1.5;
}

/* 统计数据 */
.stats-section {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 40px;
  padding-top: 60px;
  border-top: 1px solid #2a2a2a;
}

.stat-item {
  text-align: center;
  min-width: 150px;
}

.stat-number {
  font-size: 48px;
  font-weight: bold;
  color: #00aaff;
  margin-bottom: 15px;
}

.stat-label {
  font-size: 16px;
  color: #b0b0b0;
}

/* 底部 */
.home-footer {
  background-color: #121212;
  padding: 80px 0 40px;
  border-top: 1px solid #2a2a2a;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 30px;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 60px;
  margin-bottom: 40px;
}

.footer-info {
  flex: 1;
  min-width: 300px;
}

.footer-logo {
  display: flex;
  align-items: center;
  font-size: 24px;
  font-weight: bold;
  color: #00aaff;
  margin-bottom: 25px;
  gap: 15px;
}

.footer-description {
  font-size: 16px;
  line-height: 1.6;
  color: #b0b0b0;
  max-width: 400px;
}

.footer-links {
  display: flex;
  gap: 80px;
  flex-wrap: wrap;
}

.link-group {
  min-width: 180px;
}

.link-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #e0e0e0;
}

.footer-link {
  display: block;
  font-size: 16px;
  color: #b0b0b0;
  text-decoration: none;
  margin-bottom: 15px;
  transition: color 0.3s ease;
}

.footer-link:hover {
  color: #00aaff;
}

.footer-bottom {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 30px;
  text-align: center;
  padding-top: 40px;
  border-top: 1px solid #2a2a2a;
}

.copyright {
  font-size: 14px;
  color: #808080;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-section {
    padding: 80px 0;
  }

  .logo-text {
    font-size: 28px;
  }

  .hero-title {
    font-size: 36px;
  }

  .hero-buttons {
    flex-direction: column;
    gap: 20px;
    align-items: center;
  }

  .btn {
    width: 100%;
    max-width: 300px;
    text-align: center;
  }

  .features-section,
  .career-section {
    padding: 80px 0;
  }

  .features-content {
    grid-template-columns: 1fr;
  }

  .career-cards {
    grid-template-columns: repeat(2, 1fr);
  }

  .footer-content {
    flex-direction: column;
    gap: 40px;
  }

  .footer-links {
    gap: 40px;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 60px 0;
  }

  .logo-container {
    flex-direction: column;
    gap: 15px;
  }

  .logo-text {
    font-size: 24px;
  }

  .hero-title {
    font-size: 28px;
  }

  .hero-description {
    font-size: 16px;
  }

  .btn {
    padding: 14px 30px;
    font-size: 16px;
  }

  .features-section,
  .career-section {
    padding: 60px 0;
  }

  .section-title {
    font-size: 28px;
  }

  .career-cards {
    grid-template-columns: 1fr;
  }

  .stats-section {
    flex-direction: column;
    align-items: center;
    gap: 30px;
  }

  .stat-number {
    font-size: 36px;
  }
}
</style>