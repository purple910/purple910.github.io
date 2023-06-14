# mybatis 自定义分页

# utils

## OrderItemUtils (分页数据库排序字段,可以不要)
```
@Data
@ToString
public class OrderItemUtils implements Serializable {

    private static final long serialVersionUID = 1L;
    /**
     * 需要进行排序的字段
     */
    @ApiModelProperty(value = "需要进行排序的字段")
    private String column;

    /**
     * 是否正序排列，默认 true
     */
    @ApiModelProperty(value = "是否正序排列，默认true")
    private Boolean asc = true;

}
```

## RequestPageUtils (分页请求基类)
```
@Data
public class RequestPageUtils implements Serializable {

    private static final long serialVersionUID = 8545996863226528798L;

    /**
     * 每页显示条数，默认 10
     */
    @ApiModelProperty(value = "每页显示条数，默认10")
    protected Integer size = 10;

    /**
     * 当前页
     */
    @ApiModelProperty(value = "当前页,默认为1")
    protected Integer current = 1;

    /**
     * 排序字段信息
     */
    @ApiModelProperty(value = "排序字段信息")
    protected OrderItemUtils orders = new OrderItemUtils();

    /**
     * 设置起始页 1开始
     *
     * @param current
     */
    public void setCurrent(Integer current) {
        this.current = Math.max(current, this.current);
    }

    /**
     * 设置起始页大小
     *
     * @param size
     */
    public void setSize(Integer size) {
        this.size = Math.max(size, 1);
    }
}
```

## ResponsePageUtils (分页响应基类)
```
@Data
public class ResponsePageUtils<T> implements Serializable {

    private static final long serialVersionUID = 8545996863226528798L;
    /**
     * 查询数据列表
     */
    @ApiModelProperty(value = "查询数据列表")
    protected List<T> entities = Collections.emptyList();

    /**
     * 总数
     */
    @ApiModelProperty(value = "总数")
    protected Long total = 0L;

    /**
     * 每页显示条数，默认 10
     */
    @ApiModelProperty(value = "每页显示条数，默认10")
    protected Integer size = 10;

    /**
     * 当前页
     */
    @ApiModelProperty(value = "当前页,默认为1")
    protected Integer current = 1;

    /**
     * 排序字段信息
     */
    @ApiModelProperty(value = "排序字段信息")
    protected OrderItemUtils orders = new OrderItemUtils();

}
```

# DTO

## UserQueryPageInputDTO (获取前端传来的数据,同时可以在其中进行校验)
```
@ApiModel(value = "UserQueryPageInputDTO", description = "列表查询参数")
@Data
@ToString
public class UserQueryPageInputDTO extends RequestPageUtils {


    @ApiModelProperty(value = "名称", example = "test")
    private String mc;

    @ApiModelProperty(value = "学号", example = "...")
    private String xh;

    @ApiModelProperty(value = "年级", example = "2017")
    @NotBlank(message = "年级不能为空")
    private String nj;

    /**
     * 把请求dto转换为do,用户操作数据库
     *
     * @return
     */
    public UserQueryRequestPage convertToUser() {
        return new UserQueryPageInputDTO.UserQueryPageInputDTOConvert().convert(this);
    }

    private static class UserQueryPageInputDTOConvert implements DTOConvert<UserQueryPageInputDTO, UserQueryRequestPage> {
        @Override
        public UserQueryRequestPage convert(UserQueryPageInputDTO userQueryPageInputDTO) {
            UserQueryRequestPage userQueryPage = new UserQueryRequestPage();
            BeanUtils.copyProperties(userQueryPageInputDTO, userQueryPage);
            return userQueryPage;
        }
    }
    /**
     * 请求dto与响应dto的都需要有(current,size,orders),可以通过类转换来得到响应dto
     */
    public UserQueryPageOutputDTO convert(UserQueryPageInputDTO inputDTO) {
        UserQueryPageOutputDTO outputDTO = new UserQueryPageOutputDTO();
        BeanUtils.copyProperties(inputDTO, outputDTO);
        if (StringUtils.isEmpty(inputDTO.getOrders().getColumn())){
            outputDTO.setOrders(null);
        }
        return outputDTO;
    }
}
```

## UserQueryPageOutputDTO (返回前端数据)
```
@Data
public class UserQueryPageOutputDTO extends ResponsePageUtils<UserGetOutputDTO> {

    /**
     * 请求dto与响应dto的都需要有(current,size,orders),可以通过类转换来得到响应dto
     */  
    public UserQueryPageOutputDTO convert(UserQueryPageInputDTO inputDTO){
        BeanUtils.copyProperties(inputDTO, this);
        if (StringUtils.isEmpty(inputDTO.getOrders().getColumn())){
            this.setOrders(null);
        }
        return this;
    }
}
```

# DO

## 
```
@ToString
@Data
public class UserQueryRequestPage extends RequestPageUtils {

    /**
     * 名称
     */
    private String mc;

    /**
     * 学号
     */
    private String xh;

    /**
     * 年级
     */
    private String nj;

    /**
     * 开始
     */
    private Integer start;

    /**
     * 结束
     */
    private Integer end;

    /**
     * 获取开始位置
     *
     * @return
     */
    public Integer getStart() {
        return (this.current - 1) * this.size;
    }

    /**
     * 获取结束位置
     *
     * @return
     */
    public Integer getEnd() {
        return this.current * this.size;
    }

}
```

# DAO

## UserMapper 
```
@Mapper
public interface UserMapper {

    /**
     * 根据参数进行分页查询
     * @param entity
     * @return
     */
    public List<User> listByPage(UserQueryRequestPage entity);

    /**
     * 获取总条数
     * @param entity
     * @return
     */
    public int countByPage(UserQueryRequestPage entity);
}
```

## UserMapper.xml
```
    <!-- 获取分页查询的总条数  -->
    <select id="countByPage" resultType="int" parameterType="com.example.demo.service.params.UserQueryRequestPage">
        SELECT COALESCE(COUNT(1),0)
          FROM tb_user
         WHERE nj= #{nj}
           AND sfsc = 'N'
        <if test="mc != null and mc != ''">
           AND mc LIKE '%${mc}%'
        </if>
        <if test="xh!= null and xh!= ''">
           AND xhLIKE '${xh}%'
        </if>
    </select>

    <!-- 通过条件查询分页   -->
    <select id="listByPage" resultType="com.example.demo.domain.User" parameterType="com.example.demo.service.params.UserQueryRequestPage">
        SELECT * FROM (
        SELECT tmp.*, rownum row_id FROM (
        SELECT *
          FROM tb_user
           AND nj= #{nj}
        <if test="mc != null and mc != ''">
           AND mc LIKE '%${mc}%'
        </if>
        <if test="xh!= null and xh!= ''">
           AND xhLIKE '${xh}%'
        </if>
        ) tmp
         WHERE #{end} >= rownum)
         WHERE row_id > #{start}
      <!-- 如果没有排序,可以不写,或者写死 -->
        <if test="orders.column != null and orders.column != ''">
        <if test="orders.asc == true">
         ORDER BY ${orders.column} ASC
        </if>
        <if test="orders.asc == false">
         ORDER BY ${orders.column} DESC
        </if>
        </if>
    </select>
```

# Service

## UserServiceImpl
```
public class UserServiceImpl implements UserService {
      @Resource
      private UserMapper mapper;
      
    @Override
    public List<User> listByPage(UserQueryRequestPage param) {
        // 返回查询数据
        return mapper.listByPage(param);
    }

    @Override
    public int countByPage(UserQueryRequestPage param) {
        // 获取单位列表查询的总条数
        return mapper.countByPage(param);
    }

}
```

# controller

## UserController 
```
@RestController
@RequestMapping("/user")
@Api(tags = "人员管理")
public class UserController{
      @Autowired
      private UserService userService;

      @ApiOperation("获取人员列表")
      @ApiOperationSupport(order = 1)
      @PostMapping("/query")
      public R<UserQueryPageOutputDTO > query(@RequestBody @Valid UserQueryPageInputDTO requestDTO, BindingResult validateResult){
            String msg= null;
            if (result.hasErrors()) {
                  List<ObjectError> objectErrors = result.getAllErrors();
                  msg= String.valueOf(objectErrors.get(0).getDefaultMessage());
            }
            if (!StringUtils.isEmpty(msg)) {
                  return R.failed(msg);
            }

            // 定义返回类
            UserQueryPageOutputDTO outputDTO = queryPageInputDTO.convert(queryPageInputDTO);

            // 获取条数
            UserQueryRequestPage user = queryPageInputDTO.convertToUser();
            long count = userService.countByPage(user);
            if (count == 0) {
                  return R.ok(outputDTO);
            }
            outputDTO.setTotal(count);

            // 获取数据
            List<User> queryPage = userService.listByPage(user);

            // 数据转换
            if (!queryPage.isEmpty()){
                  List<UserGetOutputDTO> list = new ArrayList<>();
                  queryPage.forEach(item -> list.add(new UserGetOutputDTO().convert(item)));
                  outputDTO.setEntities(list);
            }

            // 数据返回
            return R.ok(outputDTO);
      }
}
```

### 注: @ApiModelProperty, @Api, @ApiOperation等是属于swagger的注解,如果不要可以去掉; @NotBlank, @Valid是用来校验参数的,要添加validation依赖