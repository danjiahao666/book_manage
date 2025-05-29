-- 创建数据库
CREATE DATABASE IF NOT EXISTS book_recommendation CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE book_recommendation;

-- 创建表

-- Django内置表 - auth_user
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户配置文件表
CREATE TABLE IF NOT EXISTS `users_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `avatar` varchar(100) DEFAULT NULL,
  `bio` longtext NOT NULL,
  `birth_date` date DEFAULT NULL,
  `favorite_genres` varchar(200) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `users_userprofile_user_id_fkey` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 图书分类表
CREATE TABLE IF NOT EXISTS `books_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 图书表
CREATE TABLE IF NOT EXISTS `books_book` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `author` varchar(200) NOT NULL,
  `cover` varchar(100) DEFAULT NULL,
  `isbn` varchar(13) NOT NULL,
  `description` longtext NOT NULL,
  `publisher` varchar(200) NOT NULL,
  `publish_date` date NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `pages` int(10) unsigned NOT NULL,
  `language` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `isbn` (`isbn`),
  KEY `books_book_category_id_fkey` (`category_id`),
  CONSTRAINT `books_book_category_id_fkey` FOREIGN KEY (`category_id`) REFERENCES `books_category` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 评论表
CREATE TABLE IF NOT EXISTS `books_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` longtext NOT NULL,
  `rating` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `book_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `books_comment_book_id_user_id_unique` (`book_id`,`user_id`),
  KEY `books_comment_book_id_fkey` (`book_id`),
  KEY `books_comment_user_id_fkey` (`user_id`),
  CONSTRAINT `books_comment_book_id_fkey` FOREIGN KEY (`book_id`) REFERENCES `books_book` (`id`) ON DELETE CASCADE,
  CONSTRAINT `books_comment_user_id_fkey` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `books_comment_rating_check` CHECK ((`rating` >= 1 and `rating` <= 5))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户图书交互表
CREATE TABLE IF NOT EXISTS `books_userbookinteraction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `viewed_at` datetime(6) NOT NULL,
  `view_count` int(10) unsigned NOT NULL,
  `book_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `books_userbookinteraction_user_id_book_id_unique` (`user_id`,`book_id`),
  KEY `books_userbookinteraction_book_id_fkey` (`book_id`),
  KEY `books_userbookinteraction_user_id_fkey` (`user_id`),
  CONSTRAINT `books_userbookinteraction_book_id_fkey` FOREIGN KEY (`book_id`) REFERENCES `books_book` (`id`) ON DELETE CASCADE,
  CONSTRAINT `books_userbookinteraction_user_id_fkey` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Django所需的其他必要表
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_uniq` (`app_label`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_idx` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入示例数据

-- 插入用户数据
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$260000$QhCE4qG1Spr1hBhcPtbz2q$XPWokoH36hQa1IELGu8UzDbZ/i8p0IqG0a/nZLMCPYI=', NULL, 1, 'admin', '管理员', '账户', 'admin@example.com', 1, 1, '2023-06-01 12:00:00.000000'),
(2, 'pbkdf2_sha256$260000$ux5cKEMJHnQJMf5O1hDXBu$ka5AKQhPtRzP/DZr5RNnKH+GbLo3OAGGn4Dkb7pJuI8=', NULL, 0, 'user1', '张', '三', 'user1@example.com', 0, 1, '2023-06-01 13:00:00.000000'),
(3, 'pbkdf2_sha256$260000$2Kj2CjXd7PsfPKxIGn98Uf$T5XzYIg1Gzm+pKISTQpmt4z86BoD5++TXEUhKNbMA+0=', NULL, 0, 'user2', '李', '四', 'user2@example.com', 0, 1, '2023-06-01 14:00:00.000000'),
(4, 'pbkdf2_sha256$260000$1aFlQDIRO70XWmjHKQvNnw$SNJ5HQRqG+vZoCUQ6ZJ7lJKvvdENIDduDXn+hwAHh6I=', NULL, 0, 'user3', '王', '五', 'user3@example.com', 0, 1, '2023-06-01 15:00:00.000000');

-- 插入用户配置文件
INSERT INTO `users_userprofile` (`id`, `avatar`, `bio`, `birth_date`, `favorite_genres`, `user_id`) VALUES
(1, '', '系统管理员', '1990-01-01', '科幻,历史,哲学', 1),
(2, '', '热爱阅读的读书爱好者', '1992-05-15', '科幻,悬疑,冒险', 2),
(3, '', '文学爱好者，尤其喜欢古典文学', '1985-10-20', '文学,历史,传记', 3),
(4, '', '编程爱好者，关注技术书籍', '1995-03-08', '计算机,科技,教育', 4);

-- 插入图书分类
INSERT INTO `books_category` (`id`, `name`, `description`, `created_at`) VALUES
(1, '科幻小说', '描述未来、太空、时间旅行、平行宇宙等虚构场景的作品', '2023-06-02 10:00:00.000000'),
(2, '悬疑推理', '以谜题和推理为主要内容的作品', '2023-06-02 10:01:00.000000'),
(3, '文学经典', '具有深远影响力的经典文学作品', '2023-06-02 10:02:00.000000'),
(4, '历史', '关于历史事件和历史人物的书籍', '2023-06-02 10:03:00.000000'),
(5, '计算机与编程', '编程、计算机科学和技术相关书籍', '2023-06-02 10:04:00.000000'),
(6, '哲学思想', '关于哲学观点和思想的书籍', '2023-06-02 10:05:00.000000'),
(7, '传记', '讲述名人或普通人生平的书籍', '2023-06-02 10:06:00.000000'),
(8, '商业管理', '关于商业策略和管理理论的书籍', '2023-06-02 10:07:00.000000');

-- 插入图书数据
INSERT INTO `books_book` (`id`, `title`, `author`, `cover`, `isbn`, `description`, `publisher`, `publish_date`, `price`, `pages`, `language`, `created_at`, `updated_at`, `category_id`) VALUES
(1, '三体', '刘慈欣', 'covers/santi.jpg', '9787536692930', '地球文明向宇宙发出信息，引来了三体文明的入侵，人类的命运从此改变...', '重庆出版社', '2008-01-01', 39.50, 302, '中文', '2023-06-03 10:00:00.000000', '2023-06-03 10:00:00.000000', 1),
(2, '黑暗森林', '刘慈欣', 'covers/heianselin.jpg', '9787536693968', '三体人在利用魔法般的科技锁死了地球人的科学之后，地球人面临前所未有的危机...', '重庆出版社', '2008-05-01', 42.00, 470, '中文', '2023-06-03 10:01:00.000000', '2023-06-03 10:01:00.000000', 1),
(3, '死神永生', '刘慈欣', 'covers/sishenyongsheng.jpg', '9787229030933', '地球文明和三体文明的终极对决，宇宙的命运将如何延续...', '重庆出版社', '2010-11-01', 38.00, 513, '中文', '2023-06-03 10:02:00.000000', '2023-06-03 10:02:00.000000', 1),
(4, '白夜行', '东野圭吾', 'covers/baiyexing.jpg', '9787544258609', '一桩离奇命案牵扯出跨越19年的故事，控诉了社会的疮疤...', '南海出版公司', '2013-01-01', 39.50, 538, '中文', '2023-06-03 10:03:00.000000', '2023-06-03 10:03:00.000000', 2),
(5, '嫌疑人X的献身', '东野圭吾', 'covers/xianyirenX.jpg', '9787544247252', '为了心爱的女人，数学天才石神用逻辑推理完美地设计了一个杀人案...', '南海出版公司', '2014-06-01', 35.00, 320, '中文', '2023-06-03 10:04:00.000000', '2023-06-03 10:04:00.000000', 2),
(6, '百年孤独', '加西亚·马尔克斯', 'covers/bainiangudu.jpg', '9787544253994', '布恩迪亚家族七代人的传奇故事，拉丁美洲魔幻现实主义代表作...', '南海出版公司', '2011-06-01', 39.50, 360, '中文', '2023-06-03 10:05:00.000000', '2023-06-03 10:05:00.000000', 3),
(7, '万历十五年', '黄仁宇', 'covers/wanlishiwunian.jpg', '9787108009821', '从1587年这一年的历史切片，解析明朝帝国的政治、经济、文化运行机制...', '生活·读书·新知三联书店', '1997-05-01', 18.00, 356, '中文', '2023-06-03 10:06:00.000000', '2023-06-03 10:06:00.000000', 4),
(8, 'Python编程：从入门到实践', 'Eric Matthes', 'covers/python.jpg', '9787115428028', '全面介绍Python编程，从基本概念到项目实践，是初学者的理想指南...', '人民邮电出版社', '2016-07-01', 89.00, 459, '中文', '2023-06-03 10:07:00.000000', '2023-06-03 10:07:00.000000', 5),
(9, '人类简史', '尤瓦尔·赫拉利', 'covers/renleijiangshi.jpg', '9787508647357', '从认知革命、农业革命，到科学革命，人类如何从一个平凡的物种变成了地球的主宰...', '中信出版社', '2014-11-01', 68.00, 440, '中文', '2023-06-03 10:08:00.000000', '2023-06-03 10:08:00.000000', 6),
(10, '乔布斯传', '沃尔特·艾萨克森', 'covers/qiaobusi.jpg', '9787508630069', '描述苹果创始人史蒂夫·乔布斯传奇一生的权威传记...', '中信出版社', '2011-10-24', 68.00, 560, '中文', '2023-06-03 10:09:00.000000', '2023-06-03 10:09:00.000000', 7),
(11, '从0到1', '彼得·蒂尔', 'covers/cong0dao1.jpg', '9787508649719', '硅谷创投教父彼得·蒂尔的创新方法论，探讨创业与创新的本质...', '中信出版社', '2015-01-01', 45.00, 260, '中文', '2023-06-03 10:10:00.000000', '2023-06-03 10:10:00.000000', 8),
(12, '罪与罚', '陀思妥耶夫斯基', 'covers/zuiyufa.jpg', '9787506394864', '描述一个贫苦大学生犯下谋杀罪后的心理斗争和道德救赎...', '作家出版社', '2016-08-01', 39.80, 542, '中文', '2023-06-03 10:11:00.000000', '2023-06-03 10:11:00.000000', 3),
(13, '明朝那些事儿（全套）', '当年明月', 'covers/mingchao.jpg', '9787807693987', '以通俗有趣的方式讲述明朝历史的作品集...', '北京联合出版公司', '2009-04-01', 268.00, 3200, '中文', '2023-06-03 10:12:00.000000', '2023-06-03 10:12:00.000000', 4),
(14, '算法导论', 'Thomas H.Cormen等', 'covers/suanfa.jpg', '9787111407010', '计算机算法领域的经典教材，全面介绍算法设计与分析方法...', '机械工业出版社', '2013-01-01', 128.00, 780, '中文', '2023-06-03 10:13:00.000000', '2023-06-03 10:13:00.000000', 5),
(15, '苏菲的世界', '乔斯坦·贾德', 'covers/sufei.jpg', '9787506394510', '通过一个少女的哲学课程，引领读者领略西方哲学的发展历程...', '作家出版社', '2007-09-01', 26.00, 528, '中文', '2023-06-03 10:14:00.000000', '2023-06-03 10:14:00.000000', 6);

-- 插入评论数据
INSERT INTO `books_comment` (`id`, `content`, `rating`, `created_at`, `updated_at`, `book_id`, `user_id`) VALUES
(1, '这是一部震撼人心的科幻小说，刘慈欣的想象力令人惊叹！', 5, '2023-06-04 10:00:00.000000', '2023-06-04 10:00:00.000000', 1, 2),
(2, '作为三部曲的开始，这本书奠定了宏大的宇宙背景。', 4, '2023-06-04 10:01:00.000000', '2023-06-04 10:01:00.000000', 1, 3),
(3, '黑暗森林法则是对宇宙文明互动的绝妙比喻。', 5, '2023-06-04 10:02:00.000000', '2023-06-04 10:02:00.000000', 2, 2),
(4, '三部曲的高潮，结局令人深思。', 4, '2023-06-04 10:03:00.000000', '2023-06-04 10:03:00.000000', 3, 2),
(5, '东野圭吾最好的作品之一，情节设计精妙。', 5, '2023-06-04 10:04:00.000000', '2023-06-04 10:04:00.000000', 4, 3),
(6, '数学与犯罪的完美结合，结局出人意料。', 4, '2023-06-04 10:05:00.000000', '2023-06-04 10:05:00.000000', 5, 2),
(7, '魔幻现实主义的代表作，叙事风格独特。', 5, '2023-06-04 10:06:00.000000', '2023-06-04 10:06:00.000000', 6, 3),
(8, '通过一年的历史切片，展现整个时代的特点。', 4, '2023-06-04 10:07:00.000000', '2023-06-04 10:07:00.000000', 7, 2),
(9, '非常适合Python初学者的实用指南。', 5, '2023-06-04 10:08:00.000000', '2023-06-04 10:08:00.000000', 8, 4),
(10, '宏大的历史叙事，让人类历史变得生动有趣。', 5, '2023-06-04 10:09:00.000000', '2023-06-04 10:09:00.000000', 9, 3),
(11, '了解乔布斯传奇人生的必读书籍。', 4, '2023-06-04 10:10:00.000000', '2023-06-04 10:10:00.000000', 10, 4),
(12, '关于创新和创业的深刻洞见。', 4, '2023-06-04 10:11:00.000000', '2023-06-04 10:11:00.000000', 11, 4),
(13, '俄罗斯文学经典，对人性的深刻剖析。', 5, '2023-06-04 10:12:00.000000', '2023-06-04 10:12:00.000000', 12, 3),
(14, '通俗易懂地讲述明朝历史，非常有趣。', 5, '2023-06-04 10:13:00.000000', '2023-06-04 10:13:00.000000', 13, 2),
(15, '计算机科学专业必读，内容全面但有些难度。', 4, '2023-06-04 10:14:00.000000', '2023-06-04 10:14:00.000000', 14, 4),
(16, '哲学启蒙的绝佳读物，深入浅出。', 5, '2023-06-04 10:15:00.000000', '2023-06-04 10:15:00.000000', 15, 3),
(17, '三体系列最好的一部，情节紧凑，概念宏大。', 5, '2023-06-04 10:16:00.000000', '2023-06-04 10:16:00.000000', 1, 4);

-- 插入用户图书交互数据
INSERT INTO `books_userbookinteraction` (`id`, `viewed_at`, `view_count`, `book_id`, `user_id`) VALUES
(1, '2023-06-05 10:00:00.000000', 3, 1, 2),
(2, '2023-06-05 10:01:00.000000', 2, 2, 2),
(3, '2023-06-05 10:02:00.000000', 2, 3, 2),
(4, '2023-06-05 10:03:00.000000', 5, 4, 3),
(5, '2023-06-05 10:04:00.000000', 1, 5, 2),
(6, '2023-06-05 10:05:00.000000', 3, 6, 3),
(7, '2023-06-05 10:06:00.000000', 2, 7, 2),
(8, '2023-06-05 10:07:00.000000', 4, 8, 4),
(9, '2023-06-05 10:08:00.000000', 2, 9, 3),
(10, '2023-06-05 10:09:00.000000', 1, 10, 4),
(11, '2023-06-05 10:10:00.000000', 3, 11, 4),
(12, '2023-06-05 10:11:00.000000', 2, 12, 3); 