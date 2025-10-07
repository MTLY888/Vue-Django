import random
import string
from PIL import Image, ImageDraw, ImageFont
import io
import base64


def generate_captcha(width=120, height=40, length=4):
    """
    生成验证码图片
    
    Args:
        width (int): 图片宽度，默认120
        height (int): 图片高度，默认40
        length (int): 验证码长度，默认4
    
    Returns:
        tuple: (图片的base64编码字符串, 验证码内容)
    """
    # 生成随机验证码字符串（数字+大写字母）
    captcha_chars = string.ascii_uppercase + string.digits
    captcha_text = ''.join(random.choices(captcha_chars, k=length))
    
    # 创建图片
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # 尝试使用系统字体，如果失败则使用默认字体
    try:
        # Windows系统字体
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        try:
            # 备用字体
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)
        except:
            # 使用默认字体
            font = ImageFont.load_default()
    
    # 计算文字位置
    char_width = width // length
    char_height = height // 2
    
    # 绘制每个字符
    for i, char in enumerate(captcha_text):
        # 随机字符颜色
        char_color = (
            random.randint(0, 100),
            random.randint(0, 100),
            random.randint(0, 100)
        )
        
        # 随机字符位置（稍微偏移）
        x = i * char_width + random.randint(-5, 5)
        y = char_height + random.randint(-5, 5)
        
        # 绘制字符
        draw.text((x, y), char, font=font, fill=char_color)
    
    # 添加干扰线
    for _ in range(random.randint(3, 6)):
        line_color = (
            random.randint(100, 200),
            random.randint(100, 200),
            random.randint(100, 200)
        )
        start_x = random.randint(0, width)
        start_y = random.randint(0, height)
        end_x = random.randint(0, width)
        end_y = random.randint(0, height)
        draw.line([(start_x, start_y), (end_x, end_y)], fill=line_color, width=1)
    
    # 添加干扰点
    for _ in range(random.randint(50, 100)):
        point_color = (
            random.randint(150, 255),
            random.randint(150, 255),
            random.randint(150, 255)
        )
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=point_color)
    
    # 将图片转换为base64字符串
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return img_str, captcha_text


def generate_captcha_file(filename=None):
    """
    生成验证码并保存为文件
    
    Args:
        filename (str): 保存的文件名，如果为None则自动生成
    
    Returns:
        tuple: (保存的文件路径, 验证码内容)
    """
    img_str, captcha_text = generate_captcha()
    
    # 如果没有指定文件名，自动生成
    if filename is None:
        filename = f"captcha_{random.randint(1000, 9999)}.png"
    
    # 解码base64并保存文件
    img_data = base64.b64decode(img_str)
    with open(filename, 'wb') as f:
        f.write(img_data)
    
    return filename, captcha_text

