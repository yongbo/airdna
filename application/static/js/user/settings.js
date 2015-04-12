var imageWidth, imageHeight;
var previewWidth = 80, previewHeight = 80;
var jcrop_api = null;

var uploader = new plupload.Uploader($.extend(g.pluploadDefaults, {
    browse_button: 'btn-upload-avatar',
    url: urlFor('user.upload_avatar'),
    multipart_params: {
        'csrf_token': g.csrfToken
    },
    max_file_size: '10mb',
    init: {
        // 文件添加后立即上传
        FilesAdded: function (up, files) {
            up.disableBrowse(true);
            $('.avatar-loading-percent').show();

            plupload.each(files, function () {
                uploader.start();
            });
        },

        // 上传进度
        UploadProgress: function (up, file) {
            $('.avatar-loading-percent').text(file.percent + "%");
        },

        // 上传完毕
        FileUploaded: function (up, file, info) {
            var response = $.parseJSON(info.response);

            up.disableBrowse(false);
            imageWidth = response.width;
            imageHeight = response.height;

            if (jcrop_api) {
                jcrop_api.destroy();
            }

            if (response.result) {
                $('.upload-error-info').fadeOut();
                $('.avatar-loading-percent').hide();
                $('#modal-crop-avatar').modal('show');
                $('.avatar-preview').attr('src', response.avatar_url);
                $('.avatar-to-crop')
                    .attr('src', response.avatar_url)
                    .attr({'width': imageWidth, 'height': imageHeight})
                    .onOnce('load', function () {
                        var selectRect = null;

                        if (imageWidth > imageHeight) {
                            selectRect = [(imageWidth - imageHeight) / 2.0, 0,
                                    (imageWidth + imageHeight) / 2.0, imageHeight];
                        } else {
                            selectRect = [0, (imageHeight - imageWidth) / 2.0,
                                imageWidth, (imageHeight + imageWidth) / 2.0];
                        }

                        $('.avatar-to-crop').Jcrop({
                            onChange: showPreview,
                            onSelect: showPreview,
                            aspectRatio: 1
                        }, function () {
                            jcrop_api = this;
                            this.setSelect(selectRect);
                        });
                    });
            } else {
                $('.upload-error-info').fadeOut();
                $('.avatar-loading-percent').hide();
            }
        },

        // 上传失败
        Error: function (up) {
            $('.upload-error-info').fadeOut();
            $('.avatar-loading-percent').hide();
            up.disableBrowse(false);
        }
    }
}));

uploader.init();

function showPreview(coords) {
    var rx = previewWidth / coords.w;
    var ry = previewHeight / coords.h;

    $('.jcrop-holder').css('backgroundColor', '#ffffff');
    $('.avatar-preview').css({
        width: Math.round(rx * imageWidth) + 'px',
        height: Math.round(ry * imageHeight) + 'px',
        marginLeft: '-' + Math.round(rx * coords.x) + 'px',
        marginTop: '-' + Math.round(ry * coords.y) + 'px'
    });
}

$('#modal-avatar-crop')
    .on('hidden.bs.modal', function () {
        jcrop_api.destroy();
    })
    .on('show.bs.modal', function () {
        $(this).css('display', 'block');
        var $dialog = $(this).find(".modal-dialog");
        var offset = ($(window).height() - $dialog.height()) * 0.3;
        if (offset > 0) {
            $dialog.css('margin-top', offset);
        }
    });
