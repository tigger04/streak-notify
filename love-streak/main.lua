function love.load()
    -- Configuration
    DISPLAY_TIME = 3 -- How long to show text (seconds)
    FADE_IN_TIME = 0.5 -- Fade in duration (seconds)
    FADE_OUT_TIME = 0.5 -- Fade out duration (seconds)

    -- Appearance settings
    FONT_SIZE = 28
    BACKGROUND_COLOR = {0.2, 0.2, 0.2, 0.9} -- Dark gray with slight transparency
    TEXT_COLOR = {1, 1, 1, 1} -- Pure white
    PADDING = 20
    CORNER_RADIUS = 15

    -- State variables
    font = love.graphics.newFont(FONT_SIZE)
    text = arg[1] or "Test notification"
    opacity = 0 -- Start invisible for fade in
    state = "fade_in"
    timer = 0

    -- Calculate window dimensions
    local textWidth = font:getWidth(text) + (PADDING * 2)
    local textHeight = font:getHeight() + (PADDING * 2)

    -- Window setup
    love.window.setMode(textWidth, textHeight, {
        borderless = true,
        resizable = false,
        vsync = true,
        fullscreentype = "desktop", -- This helps with focus handling
        msaa = 0, -- Disable MSAA to prevent focus issues
        minwidth = 1,
        minheight = 1
    })

    -- Center the window on screen
    local desktop_width, desktop_height = love.window.getDesktopDimensions()
    love.window.setPosition((desktop_width - textWidth) / 2, (desktop_height - textHeight) / 2)
end

-- Prevent focus when window is clicked
function love.mousepressed()
    return true
end

function love.update(dt)
    timer = timer + dt

    if state == "fade_in" then
        opacity = math.min(1, timer / FADE_IN_TIME)
        if opacity >= 1 then
            state = "display"
            timer = 0
        end
    elseif state == "display" then
        if timer >= DISPLAY_TIME then
            state = "fade_out"
            timer = 0
        end
    elseif state == "fade_out" then
        opacity = math.max(0, 1 - (timer / FADE_OUT_TIME))
        if opacity <= 0 then
            love.event.quit()
        end
    end
end

function love.draw()
    -- Draw background with current opacity
    love.graphics.setColor(BACKGROUND_COLOR[1], BACKGROUND_COLOR[2], BACKGROUND_COLOR[3], BACKGROUND_COLOR[4] * opacity)
    love.graphics.rectangle("fill", 0, 0, love.graphics.getWidth(), love.graphics.getHeight(), CORNER_RADIUS,
        CORNER_RADIUS)

    -- Draw text with current opacity
    love.graphics.setColor(TEXT_COLOR[1], TEXT_COLOR[2], TEXT_COLOR[3], TEXT_COLOR[4] * opacity)
    love.graphics.setFont(font)
    love.graphics.printf(text, PADDING, PADDING, love.graphics.getWidth() - (PADDING * 2), "center")
end
